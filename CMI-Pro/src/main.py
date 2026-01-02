import flet as ft
from views.home_view import home_content
from views.home import HomeView

def main(page: ft.Page):
    HomeView(page).render()

ft.app(target=main)
