import reflex as rx
from reflex_ai.components.code_block import code_block
from reflex_ai.selection import ClickSelectionState

def selected_code_box() -> rx.Component:
    return rx.box(
        code_block(
            rx.cond(
                ClickSelectionState.code, ClickSelectionState.code, "Select a component to edit"
            )
        ),
        class_name="flex flex-col gap-3 w-full",
    )
