from components.hero import HeroSection
from components.feature_card import FeatureCard
import flet as ft


def home_content(page: ft.Page):

    hero = HeroSection(
        title="Build Better Projects with CMI-Pro",
        subtitle="A modern platform for managing and delivering projects efficiently.",
        primary_action=lambda e: page.snack_bar.open(),
        secondary_action=lambda e: print("Docs"),
    )

    features = ft.ResponsiveRow(
        [
            FeatureCard(
                "Fast Performance",
                ft.Icons.FLASH_ON,
                "Optimized for smooth desktop performance.",
            ),
            FeatureCard(
                "Clean UI",
                ft.Icons.PALETTE,
                "Modern and consistent design language.",
            ),
            FeatureCard(
                "Cross-Platform",
                ft.Icons.DEVICES,
                "Runs on Windows, Linux, and macOS.",
            ),
            FeatureCard(
                "Scalable",
                ft.Icons.TRENDING_UP,
                "Built for long-term growth.",
            ),
        ],
        spacing=20,
    )

    return ft.Column([hero, features], spacing=32)
