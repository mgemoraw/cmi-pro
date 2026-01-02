import flet as ft


class HomeView:
    def __init__(self, page: ft.Page):
        self.page = page

        # Productivity entries and form controls
        self.entries = []
        self.equipment_dropdown = None
        self.date_picker = None
        self.operator_field = None
        self.hours_field = None
        self.units_field = None
        self.fuel_field = None
        self.notes_field = None

        self.page.scroll = "auto"

    # ---------- Utilities ----------
    def show_message(self, msg: str):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("CMI-Pro"),
            content=ft.Text(msg),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog())],
        )
        self.page.dialog.open = True
        self.page.update()

    def close_dialog(self):
        self.page.dialog.open = False
        self.page.update()

    # ---------- Layout ----------
    def render(self):
        self.page.clean()
        self.page.title = "CMI-Pro — Home"
        self.page.padding = 24
        self.page.bgcolor = ft.Colors.SURFACE

        self.page.add(
            ft.Column(
                [
                    self.header(),
                    self.hero(),
                    self.features(),
                    self.productivity_section(),
                    self.footer(),
                ],
                spacing=32,
                expand=True,
            )
        )

    # ---------- Productivity section ----------
    def productivity_section(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Equipment Productivity", size=20, weight=ft.FontWeight.BOLD),
                    self.productivity_form(),
                    ft.Divider(),
                    self.entries_table()
                ],
                spacing=12,
            ),
            padding=16,
            border_radius=12,
            bgcolor=ft.Colors.SURFACE,
        )

    def productivity_form(self):
        # Lazy init of controls so state persists across updates
        if not self.equipment_dropdown:
            equipment_options = ["Excavator", "Dozer", "Truck", "Wheel Loader", "Bulldozer"]
            
            self.equipment_dropdown =ft.Dropdown(
                width=220,
                height=60,
                options=[ft.DropdownOption(opt) for opt in equipment_options],
                value=equipment_options[0],
                label="Equipment Type",
            )
            

           
            # self.date_picker = ft.DatePicker(help_text="Date",)
            self.operator_field = ft.TextField(label="Operator", width=220)
            self.hours_field = ft.TextField(label="Operating Hours", width=160, keyboard_type=ft.KeyboardType.NUMBER, hint_text="e.g., 8.5")
            self.units_field = ft.TextField(label="Units Produced", width=160, keyboard_type=ft.KeyboardType.NUMBER)
            self.fuel_field = ft.TextField(label="Fuel Consumed (L)", width=160, keyboard_type=ft.KeyboardType.NUMBER)
            self.notes_field = ft.TextField(label="Notes", multiline=True)

        return ft.Container(
            content=ft.Column(
                [
                    ft.ResponsiveRow(
                        [
                            ft.Column(controls=[
                                self.equipment_dropdown,
                                # self.date_picker,
                            ], col={"sm":12, "md":4}),
                            ft.Column(controls=[
                                self.operator_field,
                                ft.Row([self.hours_field, self.units_field, self.fuel_field], spacing=12)
                            ], col={"sm":12, "md":6}),
                        ],
                        spacing=12
                    ),
                    self.notes_field,
                    ft.Row(
                        [
                            ft.ElevatedButton("Add Entry", on_click=self.submit_productivity),
                            ft.OutlinedButton("Clear", on_click=self.clear_form)
                        ],
                        spacing=12
                    )
                ],
                spacing=10
            ),
            padding=12,
            border_radius=10,
            bgcolor=ft.Colors.SURFACE,
        )

    def submit_productivity(self, e):
        # Basic validation
        try:
            hours = float(self.hours_field.value or 0)
            units = float(self.units_field.value or 0)
            fuel = float(self.fuel_field.value or 0)
        except ValueError:
            self.show_message("Please enter numeric values for hours, units and fuel.")
            return

        if hours <= 0:
            self.show_message("Operating hours must be > 0.")
            return

        entry = {
            # "date": str(self.date_picker.value) if self.date_picker.value else "",
            'date': "",
            "equipment": self.equipment_dropdown.value,
            "operator": (self.operator_field.value or "").strip(),
            "hours": hours,
            "units": units,
            "fuel": fuel,
            "notes": (self.notes_field.value or "").strip(),
        }
        self.entries.append(entry)
        self.clear_form()
        self.show_message("Productivity entry added.")
        self.page.update()

    def clear_form(self, e=None):
        if self.date_picker:
            self.date_picker.value = None
        if self.operator_field:
            self.operator_field.value = ""
        if self.hours_field:
            self.hours_field.value = ""
        if self.units_field:
            self.units_field.value = ""
        if self.fuel_field:
            self.fuel_field.value = ""
        if self.notes_field:
            self.notes_field.value = ""
        self.page.update()

    def entries_table(self):
        if not self.entries:
            return ft.Text("No entries yet.", color=ft.Colors.ON_SURFACE_VARIANT)

        rows = []
        for i, ent in enumerate(self.entries):
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(ent["date"] or "-")),
                        ft.DataCell(ft.Text(ent["equipment"])),
                        ft.DataCell(ft.Text(ent["operator"] or "-")),
                        ft.DataCell(ft.Text(str(ent["hours"]))),
                        ft.DataCell(ft.Text(str(ent["units"]))),
                        ft.DataCell(ft.Text(str(ent["fuel"]))),
                        ft.DataCell(ft.IconButton(ft.Icons.DELETE, tooltip="Remove", on_click=lambda e, idx=i: self.remove_entry(e, idx))),
                    ]
                )
            )

        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Date")),
                ft.DataColumn(ft.Text("Equipment")),
                ft.DataColumn(ft.Text("Operator")),
                ft.DataColumn(ft.Text("Hours")),
                ft.DataColumn(ft.Text("Units")),
                ft.DataColumn(ft.Text("Fuel (L)")),
                ft.DataColumn(ft.Text("")),
            ],
            rows=rows,
            column_spacing=12,
            border=ft.border.all(1, ft.Colors.ON_SURFACE_VARIANT),
        )

    def remove_entry(self, e, idx):
        if 0 <= idx < len(self.entries):
            self.entries.pop(idx)
            self.show_message("Entry removed.")
            self.page.update()

    # ---------- Components ----------
    def header(self):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.BUILD, color=ft.Colors.WHITE),
                            ft.Text(
                                "CMI-Pro",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Row(
                        [
                            ft.TextButton("Home", on_click=lambda e: self.show_message("You are already home")),
                            ft.TextButton("Projects", on_click=lambda e: self.show_message("Projects coming soon")),
                            ft.TextButton("Settings", on_click=lambda e: self.show_message("Settings coming soon")),
                        ],
                        spacing=12,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.symmetric(horizontal=24, vertical=14),
            bgcolor=ft.Colors.PRIMARY,
            border_radius=12,
        )

    def hero(self):
        return ft.Container(
            content=ft.ResponsiveRow(
                [
                    ft.Column(
                        col={"sm": 12, "md": 7},
                        controls=[
                            ft.Text(
                                "Productivity Norm of Water Sector Projects",
                                size=36,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                            ft.Text(
                                "Data Analysis and Management Tool.",
                                size=16,
                                color=ft.Colors.WHITE70,
                            ),
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        "Get Started",
                                        icon=ft.Icons.PLAY_ARROW,
                                        on_click=lambda e: self.show_message("Welcome to CMI-Pro"),
                                    ),
                                    ft.ElevatedButton(
                                        "Read Help Docs",
                                        on_click=lambda e: self.show_message("Help Content"),
                                    ),
                                ],
                                spacing=12,
                            ),
                        ],
                        spacing=16,
                    ),
                    ft.Container(
                        col={"sm": 12, "md": 5},
                        content=ft.Icon(
                            ft.Icons.DESKTOP_WINDOWS,
                            size=120,
                            color=ft.Colors.WHITE54,
                        ),
                        alignment=ft.Alignment.CENTER,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=36,
            border_radius=16,
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=[ft.Colors.INDIGO, ft.Colors.CYAN],
            ),
        )

    def features(self):
        features = [
            ("Fast Performance", ft.Icons.FLASH_ON, "Optimized for smooth desktop experiences."),
            ("Clean UI", ft.Icons.PALETTE, "Consistent and modern design system."),
            ("Cross-Platform", ft.Icons.DEVICES, "Runs on Windows, Linux, and macOS."),
            ("Scalable", ft.Icons.TRENDING_UP, "Built for growth and extensibility."),
        ]

        return ft.Column(
            [
                ft.Text("Key Features", size=22, weight=ft.FontWeight.BOLD),
                ft.ResponsiveRow(
                    [
                        self.feature_card(title, icon, desc)
                        for title, icon, desc in features
                    ],
                    spacing=20,
                ),
            ],
            spacing=16,
        )

    def feature_card(self, title, icon, desc):
        return ft.Container(
            col={"sm": 12, "md": 6, "lg": 3},
            padding=20,
            border_radius=14,
            bgcolor=ft.Colors.ON_SECONDARY,
            content=ft.Column(
                [
                    ft.Icon(icon, size=36, color=ft.Colors.PRIMARY),
                    ft.Text(title, weight=ft.FontWeight.BOLD),
                    ft.Text(desc, size=13, color=ft.Colors.ON_SURFACE_VARIANT),
                ],
                spacing=10,
            ),
        )

    def footer(self):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text("© 2026 CMI-Pro", size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.Row(
                        [
                            ft.IconButton(ft.Icons.GITE, tooltip="GitHub"),
                            ft.IconButton(ft.Icons.BUILD_CIRCLE, tooltip="Twitter"),
                        ]
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
        )
