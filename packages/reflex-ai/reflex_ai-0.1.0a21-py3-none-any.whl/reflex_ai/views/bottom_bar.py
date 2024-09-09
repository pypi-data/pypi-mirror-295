import reflex as rx
from reflex_ai.toolbar import ToolbarState
from reflex_ai.components import hint, icon_button


def help_icon() -> rx.Component:
    def popover_item(text: str, icon: str, link: str = "/") -> rx.Component:
        return rx.box(
            rx.link(
                rx.icon(tag=icon, size=20, stroke_width="1.5"),
                text,
                href=link,
                underline="none",
                class_name="flex items-center gap-3 hover:bg-[--slate-3] px-[0.875rem] py-2 font-base text-[--slate-10] hover:!text-[--slate-9] transition-bg overflow-hidden",
            ),
        )

    return rx.popover.root(
        rx.popover.trigger(
            rx.box(
                hint(
                    text="Support",
                    content=rx.box(
                        rx.icon(
                            tag="circle-help",
                            size=22,
                            stroke_width="1.5",
                            class_name="!text-[--slate-10]",
                        ),
                        class_name="group-data-[state=open]:bg-[--slate-3] group-hover:bg-[--slate-3] p-2 rounded-xl transition-bg cursor-help",
                    ),
                ),
                class_name="group",
            ),
        ),
        rx.popover.content(
            rx.box(
                popover_item(
                    "Documentation", "book-text", "https://reflex.dev/"
                ),  # TODO: add docs
                popover_item(
                    "Support", "life-buoy", "https://discord.com/invite/T5WSbC2YtQ"
                ),
                class_name="border-[--slate-5] bg-[--slate-1] shadow-large border border-box rounded-xl divide-y divide-[var(--slate-5)] overflow-hidden",
            ),
            side="top",
            avoid_collisions=True,
            class_name="items-center bg-transparent !shadow-none !p-0 border-none w-[214px] overflow-visible",
        ),
    )


def color_item(color: str) -> rx.Component:
    from reflex_ai.playground import SettingsState

    return rx.box(
        rx.box(
            rx.cond(
                SettingsState.color == color,
                rx.icon(tag="check", size=13, stroke_width="2.5", class_name="!text-white"),
                rx.fragment()
            ),
            class_name="w-5 h-5 rounded-full flex items-center justify-center",
            style={
                "background": f"var(--{color}-9)",
            },
        ),
        rx.text(color.capitalize(), class_name="text-[--slate-12] font-small"),
        class_name="flex items-center gap-2 rounded-md shadow-small px-3 cursor-pointer bg-[--slate-1] hover:bg-[--slate-3] transition-bg box-border h-8",
        outline=rx.cond(SettingsState.color == color, "2px solid var(--slate-12)", "1px solid var(--slate-6)"),
        on_click=SettingsState.set_color(color),
    )


def settings_icon() -> rx.Component:
    from reflex_ai.playground import SettingsState
    colors = ["violet", "yellow", "green", "blue", "orange", "red"]

    return rx.popover.root(
        rx.popover.trigger(
            rx.box(
                hint(
                    text="Settings",
                    content=rx.box(
                        rx.icon(
                            tag="cog",
                            size=22,
                            stroke_width="1.5",
                            class_name="!text-[--slate-10]",
                        ),
                        class_name="group-data-[state=open]:bg-[--slate-3] group-hover:bg-[--slate-3] p-2 rounded-xl transition-bg cursor-pointer",
                    ),
                ),
                class_name="group",
            ),
        ),
        rx.popover.content(
            rx.box(
                # Selection Color
                rx.box(
                    rx.text("Selection Color", class_name="text-[--slate-12] font-small font-medium"),
                    rx.box(
                        *[color_item(color) for color in colors],
                        class_name="grid grid-cols-2 gap-3",
                    ),
                    class_name="flex flex-col gap-3",
                ),
                # Opacity
                rx.box(
                    rx.text(f"Opacity {SettingsState.opacity[0]}", class_name="text-[--slate-12] font-small font-medium"),
                    rx.slider(min=0.75, max=1.0, step=0.025, value=SettingsState.opacity, size="1", radius="full", on_change=SettingsState.set_opacity),
                    class_name="flex flex-col gap-3",
                ),
                class_name="border-[--slate-5] bg-[--slate-1] shadow-large border border-box rounded-xl flex flex-col gap-4 overflow-hidden px-[0.875rem] py-4",
            ),
            side="top",
            align="center",
            avoid_collisions=True,
            class_name="items-center bg-transparent !shadow-none !p-0 border-none w-[254px] overflow-visible",
        ),
    )


def textarea_prompt() -> rx.Component:
    return rx.form(
        rx.el.textarea(
            name="prompt",
            placeholder=rx.cond(
                ToolbarState.step == 2,
                "Ask me for any follow up changes...",
                "Ask me to change anything...",
            ),
            max_length=1000,
            # autofocus=True,
            enter_key_submit=True,
            disabled=ToolbarState.processing,
            class_name="border-[--slate-5] bg-[--white-1] p-[0.5rem_2.5rem_0.5rem_0.75rem] border rounded-[0.75rem] focus:ring-2 focus:ring-[--violet-9] ring-offset-0 w-full h-24 scrollbar-width-thin font-base text-[--slate-11] placeholder:text-[--slate-9] main-textarea outline-none resize-none",
        ),
        rx.cond(
            ~ToolbarState.processing,
            hint(
                text="Submit",
                content=icon_button(
                    icon="arrow-up",
                    class_name="right-3 bottom-2 !absolute",
                    style={
                        "textarea:placeholder-shown + &": {
                            "opacity": "0.65",
                            "cursor": "not-allowed",
                            # "pointer-events": "none",
                            "_hover": {
                                "background": "linear-gradient(180deg, var(--violet-9) 0%, var(--violet-10) 100%)"
                            },
                        },
                    },
                ),
            ),
            hint(
                text="Cancel",
                content=icon_button(
                    icon="square",
                    variant="destructive",
                    class_name="right-3 bottom-2 !absolute",
                ),
            ),
        ),
        # reset_on_submit=True,
        on_submit=ToolbarState.process,
        class_name="relative flex flex-col justify-end gap-3 w-full h-auto max-h-[160px]",
    )


# Bottom bar
def bottom_bar() -> rx.Component:
    from reflex_ai.playground import SettingsState

    return (
        rx.box(
            textarea_prompt(),
            rx.box(
                hint(
                    text="Hide sidebar",
                    content=rx.box(
                        rx.icon(
                            tag="panel-right-open",
                            size=20,
                            stroke_width="1.5",
                            class_name="shrink-0",
                            rotate=rx.cond(
                                SettingsState.side == "right", "180deg", "0deg"
                            ),
                        ),
                        class_name="hover:bg-[--slate-3] p-2 rounded-xl text-[--slate-10] transition-bg cursor-pointer",
                        on_click=SettingsState.setvar("is_open", ~SettingsState.is_open),
                    ),
                ),
                hint(
                    text="Select and edit",
                    content=rx.box(
                        rx.icon(
                            tag="square-mouse-pointer",
                            size=20,
                            stroke_width="1.5",
                            class_name="shrink-0",
                        ),
                        class_name="hover:bg-[--slate-3] p-2 rounded-xl text-[--slate-10] transition-bg cursor-pointer",
                    ),
                ),
                hint(
                    text=f"Move to {rx.cond(SettingsState.side == 'right', 'left', 'right')}",
                    content=rx.box(
                        rx.icon(
                            tag="arrow-left-to-line",
                            size=20,
                            stroke_width="1.5",
                            class_name="shrink-0",
                            rotate=rx.cond(
                                SettingsState.side == "right", "0deg", "180deg"
                            ),
                        ),
                        class_name="hover:bg-[--slate-3] p-2 rounded-xl text-[--slate-10] transition-bg cursor-pointer",
                        on_click=SettingsState.toggle_side,
                    ),
                ),
                rx.spacer(),
                settings_icon(),
                help_icon(),
                class_name="flex flex-row items-center gap-3 w-full",
            ),
            class_name="flex flex-col gap-3 w-full",
        ),
    )
