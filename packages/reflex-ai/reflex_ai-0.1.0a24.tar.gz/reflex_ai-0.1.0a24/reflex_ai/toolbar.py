"""The local AI toolbar to hook up with the server-side reflex agent."""

import json
import os

import httpx
import reflex as rx
import difflib
from flexai.message import Message, UserMessage
from flexai.tool import ToolCall, ToolResult, parse_tool_item
from reflex_ai.selection import ClickSelectionState
from reflex_ai.local_agent import (
    get_agent,
    InternRequest,
    InternResponse,
    ToolRequestResponse,
    EditResult,
    directory_diff,
)
from reflex_ai import utils, paths
from typing import Any, Type

# Tools mapping to human readable names
tools_hr_names = {
    "get_module_source": "Analyzing code",
    "add_python_element": "Adding new elements",
    "update_python_element": "Updating elements",
    "delete_python_element": "Deleting elements",
}

def authorization_header(token: str) -> dict[str, str]:
    """Construct an authorization header with the specified token as bearer token.

    Args:
        token: The access token to use.

    Returns:
        The authorization header in dict format.
    """
    return {"Authorization": f"Bearer {token}"}


async def make_request(
        endpoint: str,
        data: dict,
        url: str = os.getenv("FLEXGEN_BACKEND_URL", "http://localhost:8000"),
        timeout: int = 60,
) -> dict:
    """Make a request to the backend.

    Args:
        endpoint: The endpoint to send the request to.
        data: The data to send.
        url: The URL of the backend.
        timeout: The timeout for the request.

    Returns:
        The JSON response from the backend.
    """
    from reflex_cli.utils import hosting

    token, _ = hosting.get_existing_access_token()
    headers = authorization_header(token)

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{url}/api/{endpoint}",
            data=data,
            headers=headers,
            timeout=timeout,
        )

    print(resp)
    print(resp.json())
    resp.raise_for_status()
    return resp.json()


class Diff(rx.Base):
    filename: str
    diff: str

class ToolbarState(rx.State):
    """The toolbar state."""

    tools_used: list[str] = ["Preparing request"]
    current_step: str = "selected_code" # The current step name of the process (selected_code, processing, review_changes)
    processing: bool = False
    selected_id: str = ""
    code: str = ""
    prompt: str = ""
    step: int = 0
    diff: list[Diff] = []
    selected_diff: Diff = Diff(filename="", diff="") # The selected diff
    changes_comment: str = ""
    edit_id: str = ""

    @rx.background
    async def process(self, prompt: dict[str, str]):
        """Process the user's prompt.

        Args:
            prompt: The prompt from the user from the form input.
        """
        # Set the processing flag to True.
        async with self:
            self.start_processing()
            self.prompt = prompt["prompt"]
            selection_state = await self.get_state(ClickSelectionState)
        yield

        # Get the selected code.
        selected_code = "\n".join(selection_state._selected_code)

        # Create the intern request.
        request = InternRequest(
            prompt=prompt["prompt"],
            selected_code=selected_code,
            selected_module=selection_state.selected_module,
            selected_function=selection_state.selected_function,
        )
        response = await make_request("intern", request.model_dump_json())
        resp_obj = InternResponse(**response)
        messages = [Message(role=m.role, content=m.content) for m in resp_obj.messages]

        # Process the messages with the local agent.
        local_intern = get_agent()

        # Hack until we have state maintain between hot reloads.
        async with self:
            self.edit_id = resp_obj.request_id

        # Run in a loop until we're done with the request.
        while True:
            # Get any tool use messages from the intern and process them.
            tool_responses = []
            for message in messages:
                if not isinstance(message.content, list):
                    continue

                # Go through each entry in the content: could be a tool use or tool result
                for entry in message.content:

                    full_item = parse_tool_item(entry)

                    if isinstance(full_item, ToolCall):
                        # Populate to the local list of used tools
                        async with self:
                            self.tools_used.append(tools_hr_names.get(full_item.name, full_item.name))
                            print("tools used", self.tools_used)
                        yield

                        # Invoke the tool and get the response.
                        tool_response = await local_intern.invoke_tool(full_item)

                        # If there was a code change, we must validate it
                        if not tool_response.is_error and full_item.name in ["add_python_element", "update_python_element", "delete_python_element"]:
                            suggested_ndiff = tool_response.result
                            parent = self.get_value(selection_state.modules)[0]

                            try:
                                self.validate_diff_and_write(parent, suggested_ndiff)
                            except Exception as e:
                                tool_response = ToolResult(tool_response.tool_use_id, str(e), execution_time=0, is_error=True)
                                print("hit an error", e)
                            else:
                                # Turn the ndiff into a unified_diff
                                previous_source = ''.join(difflib.restore(suggested_ndiff, 1))
                                new_source = ''.join(difflib.restore(suggested_ndiff, 2))
                                suggested_unified_diff = '\n'.join(difflib.unified_diff(previous_source.splitlines(), new_source.splitlines()))
                                tool_response = ToolResult(tool_response.tool_use_id, suggested_unified_diff, tool_response.execution_time)

                        tool_responses.append(tool_response)
                        print("response", tool_responses[-1])
                    
                    elif isinstance(full_item, ToolResult):
                        # For now: don't do anything. Maybe this should be added to the used tool list
                        print("the server came to us with this response", full_item)
                        tool_responses.append(full_item)
                    
                    else:
                        print("unfortunately it is not a tool call")

                # Diff the directories.
                async with self:
                    self.load_diff()

            # Base case: no more messages to process.
            if not tool_responses:
                break

            # Send the tool response to the intern.
            tool_response_request = ToolRequestResponse(
                request_id=resp_obj.request_id,
                messages=tool_responses,
            )
            response = await make_request(
                "intern/tool_response", tool_response_request.model_dump_json()
            )
            messages = [Message(**m) for m in response]

        async with self:
            self.finish_processing(messages)
        yield
        # Touch the rxconfig.py to trigger a hot reload.
        self.trigger_reload()

    def validate_diff_and_write(self, parent: dict[str, any], suggested_ndiff: list[str]):
        """
        Given a filename, and a diff on that filename, see if the diff is valid and update the content of the file if so.
        """
        import importlib.util

        # Load the module from the filename
        filename = parent["filename"]
        module_name = os.path.splitext(os.path.basename(filename))[0]
        spec = importlib.util.spec_from_file_location(module_name, filename)
        module = importlib.util.module_from_spec(spec)
        os.environ["PYTEST_CURRENT_TEST"] = "True"

        # obtain the new source code
        new_source = ''.join(difflib.restore(suggested_ndiff, 2))

        spec.loader.exec_module(module)
        component_fn = getattr(module, parent["function"])


        # hack: don't try execing with reflex_ai.enable
        import builtins
        def noop(*args):
            pass
        original_import = builtins.__import__
        def custom_import(name, globals=None, locals=None, fromlist=(), level=0):
            module = original_import(name, globals, locals, fromlist, level)
            if name == 'reflex_ai' and 'enable' in fromlist:
                module.enable = noop
            return module
        builtins.__import__ = custom_import

        env = {}
        exec(new_source, env, env)
        eval(f"{component_fn.__name__}()", env, env)
        builtins.__import__ = original_import

        # This code has passed: write it into the file
        with open(filename, "w") as file:
            import black
            content = black.format_str(new_source, mode=black.FileMode())
            content = content.replace("(rx.State)", "(EditableState)")
            if "from reflex_ai import EditableState" not in content:
                content = f"from reflex_ai import EditableState\n{content}"
            file.write(content)

        return

    def start_processing(self):
        self.tools_used = [self.tools_used[0]]
        self.processing = True
        self.current_step = "processing"
        self.step = 1

    def finish_processing(self, messages):
        self.selected_diff = self.diff[0]
        self.changes_comment = json.dumps(messages[-1].content)
        self.current_step = "review_changes"
        self.step = 2
        self.processing = False

    async def accept_change(self):
        """Accept the current diff."""
        print("Accepting changes.")
        await make_request("intern/edit_result", data=EditResult(request_id=self.edit_id, diff=json.dumps([d.dict() for d in self.diff]), accepted=True).model_dump_json())
        print("sent request")
        diff = self.diff
        self.reset()
        utils.commit_scratch_dir(paths.base_paths[0], [d.filename for d in diff])

    async def revert_change(self):
        """Revert the current diff."""
        # Rewrite the scratch directory.
        print("Reverting changes.")
        await make_request("intern/edit_result", data=EditResult(request_id=self.edit_id, diff=json.dumps([d.dict() for d in self.diff]), accepted=False).model_dump_json())
        utils.create_scratch_dir(paths.base_paths[0], overwrite=True)
        print("sent request")
        self.reset()
        self.trigger_reload()

    def trigger_reload(self):
        """Trigger a hot reload."""
        config = rx.config.get_config()
        app_name = config.app_name
        filename = f"{app_name}/{app_name}.py"
        contents = open(filename).read()
        with open(filename, "w") as f:
            f.write(contents)

    def load_diff(self):
        diff = directory_diff()
        self.diff = [Diff(filename=str(filename), diff="\n".join(diff)) for filename, diff in diff.items()]
