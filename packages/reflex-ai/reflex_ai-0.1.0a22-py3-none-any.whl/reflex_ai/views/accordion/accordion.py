import reflex as rx
from reflex_ai.components import hint
from reflex_ai.views.accordion.selected_code_box import selected_code_box
from reflex_ai.views.accordion.process_box import process_box
from reflex_ai.views.accordion.diff_box import diff_box
from reflex_ai.toolbar import ToolbarState
from reflex_ai.views.bottom_bar import bottom_bar


def accordion_trigger(text: str, icon: str, value: str, index: int) -> rx.Component:
    from reflex_ai.playground import SettingsState
    return rx.accordion.trigger(
        rx.accordion.header(
            text,
            rx.box(
                rx.icon(
                    tag=icon,
                    size=17,
                    class_name="shrink-0",
                    color=rx.cond(
                        index >= ToolbarState.step, "var(--slate-11)", "white"
                    ),
                ),
                class_name="inline-flex absolute justify-center items-center rounded-full w-7 h-7 -start-[2.685rem]",
                background_color=rx.cond(
                    index >= ToolbarState.step, "var(--slate-4)", "var(--green-9)"
                ),
            ),
            class_name="relative font-base !leading-7 overflow-visible",
        ),
        rx.icon(
            tag="chevrons-up-down",
            size=20,
            stroke_width="1.5",
            class_name="group-data-[state=open]:text-[--slate-12] group-hover:text-[--slate-12] text-[--slate-11] transition-color",
        ),
        on_click=ToolbarState.setvar(
            "current_step", rx.cond(value == ToolbarState.current_step, "", value)
        ),
        class_name="justify-between items-center hover:!bg-[--slate-3] !px-3 !py-0 rounded-lg w-full !text-[--slate-12] transition-bg group",
    )


def accordion_item(
    text: str, icon: str, content: rx.Component, value: str, index: int
) -> rx.Component:
    return rx.accordion.item(
        accordion_trigger(text, icon, value, index),
        rx.accordion.content(
            content,
            class_name="relative !p-0 before:!h-4 after:!h-0",
        ),
        value=value,
        style={
            "border-width": "0 0 0 2px",
            "border-image": rx.cond(
                index < ToolbarState.step,
                "linear-gradient(180deg, var(--green-9) 0%, var(--green-9) 100%)",
                rx.cond(
                    index == ToolbarState.step,
                    "linear-gradient(180deg, var(--green-9) 0%, var(--slate-3) 100%)",
                    "linear-gradient(180deg, var(--slate-5) 100%, var(--slate-5) 100%)",
                ),
            ),
            "border-image-slice": "1",
            "border-style": "solid",
        },
        class_name="relative !mt-0 [&:not(:last-child)]:pb-4 pl-4 !overflow-visible",
        opacity=rx.cond(index > ToolbarState.step, 0.5, 1),
        pointer_events=rx.cond(index > ToolbarState.step, "none", "auto"),
    )


def accordion() -> rx.Component:
    return rx.box(
        rx.accordion.root(
            accordion_item(
                "Selected Code", "code-xml", selected_code_box(), "selected_code", 0
            ),
            accordion_item("Processing", "ellipsis", process_box(), "processing", 1),
            accordion_item("Review Changes", "eye", diff_box(), "review_changes", 2),
            variant="ghost",
            collapsible=True,
            default_value="selected_code",
            value=ToolbarState.current_step,
            class_name="pl-4 !rounded-none overflow-visible",
        ),
        # Bottom bar
        bottom_bar(),
        class_name="relative flex flex-col justify-between gap-4 border-[--slate-4] bg-[--slate-1] shadow-large p-4 pb-2 border rounded-[1.25rem] w-[300px] md:w-[350px] lg:w-[375px] xl:w-[400px] 2xl:w-[425px] h-[calc(100vh-2rem)] overflow-y-auto",
    )
