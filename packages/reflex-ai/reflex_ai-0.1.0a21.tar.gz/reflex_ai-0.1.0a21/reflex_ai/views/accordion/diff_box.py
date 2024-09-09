import reflex as rx
from reflex_ai.components import button
from reflex_ai.components import code_block
from reflex_ai.components import icon_button
from reflex_ai.components import hint
from reflex_ai.toolbar import ToolbarState


def dialog(trigger: rx.Component, content: rx.Component) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            trigger,
        ),
        rx.dialog.content(
            content,
            class_name="bg-[--white-1] p-4 rounded-[1.625rem] w-[26rem]",
        ),
    )


def confirm_box() -> rx.Component:
    return rx.box(
        rx.text(
            "Do you accept the changes?",
            class_name="font-base text-[--slate-11] text-balance",
        ),
        hint(
            text="Accept",
            content=dialog(
                trigger=icon_button("check", variant="success"),
                content=rx.box(
                    rx.box(
                        rx.text(
                            "Apply the changes",
                            class_name="font-medium text-[--slate-12] text-xl leading-7 tracking-[-0.01875rem]",
                        ),
                        rx.text(
                            "All your current changes will be applied. Are you sure you want to continue?",
                            class_name="font-base text-[--slate-10]",
                        ),
                        class_name="flex flex-col gap-1 w-full font-instrument-sans",
                    ),
                    rx.box(
                        rx.dialog.close(
                            button(
                                "Apply",
                                variant="success",
                                on_click=ToolbarState.accept_change,
                            ),
                        ),
                        rx.dialog.close(
                            button(
                                "Cancel",
                                variant="secondary",
                            ),
                        ),
                        class_name="flex flex-row justify-between items-center gap-3 w-full",
                    ),
                    class_name="flex flex-col gap-4",
                ),
            ),
        ),
        hint(
            text="Reject",
            content=dialog(
                trigger=icon_button("x", variant="destructive"),
                content=rx.box(
                    rx.box(
                        rx.text(
                            "Start a new session",
                            class_name="font-medium text-[--slate-12] text-xl leading-7 tracking-[-0.01875rem]",
                        ),
                        rx.text(
                            "All your current changes will be discarded. Are you sure you want to continue?",
                            class_name="font-base text-[--slate-10]",
                        ),
                        class_name="flex flex-col gap-1 w-full font-instrument-sans",
                    ),
                    rx.box(
                        rx.dialog.close(
                            button(
                                "Continue",
                                variant="destructive",
                                on_click=ToolbarState.revert_change,
                            ),
                        ),
                        rx.dialog.close(
                            button("Cancel", variant="secondary"),
                        ),
                        class_name="flex flex-row justify-between items-center gap-3 w-full",
                    ),
                    class_name="flex flex-col gap-4",
                ),
            ),
        ),
        hint(
            text="Regenerate",
            content=icon_button(
                icon="refresh-ccw",
                variant="secondary",
                on_click=ToolbarState.process({"prompt": ToolbarState.prompt}),
            ),
        ),
        class_name="flex flex-row justify-end items-end gap-3 mt-2 w-full",
    )


def diff_pill(diff) -> rx.Component:
    return rx.box(
        diff.filename.split("/")[-1],
        class_name="border-[--slate-5] hover:bg-[--slate-3] px-3 py-[0.275rem] border rounded-[62.5rem] font-small text-[--slate-11] cursor:pointer transition-bg cursor-pointer",
        background_color=rx.cond(
            ToolbarState.selected_diff == diff,
            "var(--slate-3)",
            "var(--slate-1)",
        ),
        on_click=ToolbarState.set_selected_diff(diff),
    )


def diff_pill_active(text: str) -> rx.Component:
    return rx.box(
        text,
        class_name="border-[--slate-5] bg-[--slate-3] px-3 py-[0.275rem] border rounded-[62.5rem] font-small text-[--slate-11] cursor:pointer transition-bg cursor-pointer",
    )


def diff_pills_stack() -> rx.Component:
    return rx.box(
        rx.foreach(ToolbarState.diff, lambda diff: diff_pill(diff)),
        class_name="flex flex-row flex-wrap gap-2 max-h-[300px] overflow-y-auto",
    )


def diff_box() -> rx.Component:
    return rx.box(
        # TODO: Make a summary of the changes
        # rx.el.ul(
        #     rx.el.li("Modified background color to black"),
        #     rx.el.li("Added a new button"),
        #     rx.el.li("Changed the font size"),
        #     class_name="flex flex-col gap-[0.375rem] p-0 pl-[1.25rem] font-base text-[--slate-11] list-disc",
        # ),
        rx.text(ToolbarState.changes_comment, class_name="font-base text-[--slate-11] m-h-[100px] overflow-y-auto"),
        diff_pills_stack(),
        code_block(
            ToolbarState.selected_diff.diff,
        ),
        confirm_box(),
        class_name="flex flex-col gap-3 w-full h-full overflow-hidden",
    )
