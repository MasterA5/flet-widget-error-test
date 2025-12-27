import flet as ft

from BubbleText import AnimatedTextBubble


@ft.component
def App(page: ft.Page):
    text = [
        "### 🌟 What is Flet?\n\n"
        "**Flet** is a framework in Python for building web, desktop, and mobile apps.\n\n"
        "### Features\n"
        "- Cross-platform\n"
        "- Easy to use\n"
        "- Based on Flutter\n\n"
        "```python\n"
        "import flet as ft\n"
        "def main(page: ft.Page):\n"
        "    page.bgcolor = ft.colors.BLACK\n"
        "    page.add(ft.Text('Hello Flet'))\n"
        "ft.app(target=main)\n"
        "```\n\n"
        "Official link: [flet.dev](https://flet.dev)\n"
        "Github Repo: [flet-dev](https://github.com/flet-dev/flet)"
    ]

    bubble = AnimatedTextBubble(texts=text)

    return ft.SafeArea(content=ft.Column(controls=[bubble]))


# App Entry Point
def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.render(lambda: App(page))


ft.run(main)
