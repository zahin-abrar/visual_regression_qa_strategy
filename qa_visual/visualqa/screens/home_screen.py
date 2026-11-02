"""Home screen object for the single approved Android scenario."""

from __future__ import annotations

from visualqa.components.article_card import ArticleCard


class HomeScreen:
    def __init__(self, driver):
        self.driver = driver

    @property
    def article_card(self) -> ArticleCard:
        return ArticleCard(self.driver)
