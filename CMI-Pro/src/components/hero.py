import flet as ft


class HeroSection(ft.BaseControl):
    def __init__(
        self,
        title: str,
        subtitle: str,
        primary_action,
        secondary_action=None,
    ):
        super().__init__()
        self.title = title
        self.subtitle = subtitle
        self.primary_action = primary_action
        self.secondary_action = secondary_action

    def build(self):
        return ft.Container(
            padding=36,
            border_radius=16,
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=[ft.Colors.INDIGO, ft.Colors.CYAN],
            ),
            content=ft.ResponsiveRow(
                [
                    ft.Column(
                        col={"sm": 12, "md": 7},
                        spacing=16,
                        controls=[
                            ft.Text(
                                self.title,
                                size=36,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                            ft.Text(
                                self.subtitle,
                                size=16,
                                color=ft.Colors.WHITE70,
                            ),
                            ft.Row(
                                spacing=12,
                                controls=[
                                    ft.ElevatedButton(
                                        "Get Started",
                                        icon=ft.Icons.PLAY_ARROW,
                                        on_click=self.primary_action,
                                    ),
                                    ft.OutlinedButton(
                                        "Learn More",
                                        on_click=self.secondary_action,
                                    )
                                    if self.secondary_action
                                    else ft.Container(),
                                ],
                            ),
                        ],
                    ),
                    ft.Container(
                        col={"sm": 12, "md": 5},
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            ft.Icons.DESKTOP_WINDOWS,
                            size=120,
                            color=ft.Colors.WHITE54,
                        ),
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
