import reflex as rx
from reflex_ai.toolbar import ToolbarState
from reflex_ai.views.accordion.accordion import accordion
from reflex_ai.components.styles import get_main_styles


class SettingsState(rx.State):
    is_open: bool = False
    side: str = "right"
    color: str = "violet"
    opacity: list[float] = [1.0]

    def toggle_side(self):
        self.side = "left" if self.side == "right" else "right"

    def set_opacity(self, value: list):
        self.opacity = value


def hide_button_outter() -> rx.Component:
    return rx.el.button(
        rx.icon(
            tag="panel-right-open",
            stroke_width="1.5",
            class_name="text-[--slate-11] shrink-0",
            rotate=rx.cond(SettingsState.side == "right", "0deg", "180deg"),
            size=20,
        ),
        on_click=SettingsState.setvar("is_open", ~SettingsState.is_open),
        class_name="top-1/2 inline-flex fixed justify-center items-center border-[--slate-5] bg-[--slate-1] hover:bg-[--slate-3] shadow-medium px-3 py-[0.275rem] border border-r-0 w-7 h-7 transition-bg cursor-pointer",
        border_radius=rx.cond(
            SettingsState.side == "left", "0 0.35rem 0.35rem 0", "0.35rem 0 0 0.35rem"
        ),
        right=rx.cond(SettingsState.side == "right", "0px", "auto"),
        left=rx.cond(SettingsState.side == "left", "0px", "auto"),
        display=rx.cond(SettingsState.is_open, "none", "flex"),
    )


def playground(page) -> rx.Component:
    return rx.box(
        page(),
        get_main_styles(),
        rx.el.style(
            f"""
:root {{
    --select-bg: var(--{SettingsState.color}-a4);
    --select-outline: var(--{SettingsState.color}-9);
}}
"""
        ),
        hide_button_outter(),
        rx.box(
            accordion(),
            transform=rx.cond(
                SettingsState.is_open,
                "translateX(0%)",
                rx.cond(
                    SettingsState.side == "right",
                    "translateX(100%)",
                    "translateX(-100%)",
                ),
            ),
            transition="transform 0.275s ease-out",
            opacity=SettingsState.opacity[0],
            class_name="z-[9999] fixed h-full overflow-hidden top-4 will-change-transform",
            right=rx.cond(
                SettingsState.side == "right",
                rx.cond(SettingsState.is_open, "1rem", "0px"),
                "auto",
            ),
            left=rx.cond(
                SettingsState.side == "left",
                rx.cond(SettingsState.is_open, "1rem", "0px"),
                "auto",
            ),
            pointer_events=rx.cond(SettingsState.is_open, "auto", "none"),
        ),
        on_mount=ToolbarState.load_diff,
    )
