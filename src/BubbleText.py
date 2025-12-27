import asyncio
from typing import List, Union

import flet as ft


@ft.component
def AnimatedTextBubble(
    texts: Union[str, List[str]] = "",
    speed: Union[int, float] = 10,
    pause: Union[int, float] = 0.0,
    bgcolor: ft.ColorValue = ft.Colors.GREY_900,
    border_radius: Union[int, ft.BorderRadius] = 20,
    markdown_code_theme: ft.MarkdownCodeTheme = ft.MarkdownCodeTheme.ATOM_ONE_DARK,
    markdown_extension_set: ft.MarkdownExtensionSet = ft.MarkdownExtensionSet.GITHUB_WEB,
    border: ft.Border | None = None,
):
    message_values, set_message_values = ft.use_state([])
    message_values_ref = ft.use_ref(message_values)
    running_ref = ft.use_ref(False)
    clipboard_ref = ft.use_ref(ft.Clipboard())

    message_values_ref.current = message_values

    text_list = [texts] if isinstance(texts, str) else list(texts)

    async def copy_to_clipboard(e):
        full_text = "\n".join(text_list)

        clean_text = (
            full_text.replace("#", "")
            .replace("*", "")
            .replace("`", "")
            .strip()
        )

        await clipboard_ref.current.set(clean_text)

        sb = ft.SnackBar(
            content=ft.Text("✅ Copied to clipboard", color=ft.Colors.WHITE),
            bgcolor=bgcolor,
        )

        ft.context.page.show_dialog(sb)
        ft.context.page.update()

    async def type_text(full_text: str):
        current = message_values_ref.current
        new_messages = current + [""]
        set_message_values(new_messages)
        message_values_ref.current = new_messages
        msg_index = len(new_messages) - 1

        partial_text = ""
        for ch in full_text:
            if not running_ref.current:
                break
            partial_text += ch
            current = message_values_ref.current
            updated_messages = list(current)
            updated_messages[msg_index] = partial_text
            set_message_values(updated_messages)
            message_values_ref.current = updated_messages
            await asyncio.sleep(1 / speed)

        if pause > 0 and running_ref.current:
            await asyncio.sleep(pause)

    async def type_loop():
        for text in text_list:
            if not running_ref.current:
                break
            await type_text(text)

    def start_typing():
        running_ref.current = True
        set_message_values([])
        message_values_ref.current = []
        asyncio.create_task(type_loop())

        def stop_typing():
            running_ref.current = False

        return stop_typing

    ft.use_effect(start_typing, [tuple(text_list), speed, pause])

    return ft.Container(
        adaptive=True,
        expand=True,
        expand_loose=True,
        padding=10,
        ink=True,
        border=border,
        border_radius=border_radius,
        bgcolor=bgcolor,
        on_long_press=copy_to_clipboard,
        content=ft.Column(
            spacing=2,
            tight=False,
            controls=[
                ft.Markdown(
                    value=value,
                    selectable=True,
                    extension_set=markdown_extension_set,
                    code_theme=markdown_code_theme,
                    on_tap_link=lambda e: ft.context.page.launch_url(e.data),
                )
                for value in message_values
            ],
        ),
    )
