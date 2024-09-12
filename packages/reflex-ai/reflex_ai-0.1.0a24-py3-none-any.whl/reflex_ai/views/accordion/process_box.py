import reflex as rx
from reflex_ai.toolbar import ToolbarState


def tl_item(text: str) -> rx.Component:
    return rx.cond(
        (text == ToolbarState.tools_used[-1]) & ToolbarState.processing,
        rx.el.li(
            rx.box(
                rx.spinner(size="1"),
                class_name="left-[-0.65rem] absolute flex justify-center items-center bg-[--slate-4] p-[0.225rem] rounded-full w-5 h-5",
            ),
            text,
            class_name="text-[--slate-11]",
        ),
        rx.el.li(
            rx.box(
                rx.icon(tag="check", size=13),
                class_name="left-[-0.65rem] absolute flex justify-center items-center bg-[--green-4] p-[0.225rem] rounded-full w-5 h-5",
            ),
            text,
            class_name="text-[--green-10]",
        ),
    )

def process_box() -> rx.Component:
    return rx.box(
        rx.box(
            rx.el.ol(
                rx.foreach(ToolbarState.tools_used, tl_item),
                class_name="relative flex flex-col gap-4 border-[--green-5] p-0 pl-6 border-l-[1.5px] font-small text-[--slate-11] list-none",
            ),
            class_name="ps-4",
        ),
        class_name="flex flex-col w-full",
    )
