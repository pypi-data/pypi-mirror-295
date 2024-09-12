import reflex as rx


def code_block(code: str, language: str = "python") -> rx.Component:
    return rx.box(
        rx.code_block(
            code,
            language=language,
            # wrap_long_lines=True,
            class_name="code-block",
        ),
        class_name="flex flex-col gap-3 w-full h-full overflow-hidden",
    )