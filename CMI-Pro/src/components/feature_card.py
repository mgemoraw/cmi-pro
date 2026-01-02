import flet as ft


class FeatureCard(ft.BaseControl):
    def __init__(self, title: str, icon: str, description: str):
        super().__init__()
        self.title = title
        self.icon = icon
        self.description = description

    def build(self):
        return ft.Container(
            col={"sm": 12, "md": 6, "lg": 3},
            padding=20,
            border_radius=14,
            bgcolor=ft.Colors.SURFACE_VARIANT,
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Icon(self.icon, size=36, color=ft.Colors.PRIMARY),
                    ft.Text(self.title, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        self.description,
                        size=13,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                ],
            ),
        )
