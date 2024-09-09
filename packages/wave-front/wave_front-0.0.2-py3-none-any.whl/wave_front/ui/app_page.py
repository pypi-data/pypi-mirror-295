import asyncio
from abc import ABC, abstractmethod
from typing import List

from h2o_wave import Q, Zone

from .card import Card
from .scaffold import Scaffold


class AppPage(ABC):

    def __init__(self, q: Q, cache_on_load: bool = False):
        self.q = q
        self.cache_on_load = cache_on_load
        self.clear_cards()
        self.q.page['meta'] = self.scaffold().meta_card(self.zones())

        for card in self.cards():
            card.show()

        asyncio.ensure_future(self._on_load())

    @abstractmethod
    def scaffold(self) -> Scaffold:
        pass

    @abstractmethod
    def zones(self) -> List[Zone]:
        pass

    @abstractmethod
    def cards(self) -> List[Card]:
        pass

    @abstractmethod
    async def on_load(self):
        pass

    async def _on_load(self):
        cache_key = f"{self.__class__.__name__}_cached"

        if self.q.client[cache_key]:
            return

        await self.on_load()

        self.q.client[cache_key] = self.cache_on_load

    def clear_cards(self):
        if not self.q.client.cards:
            return

        for name in self.q.client.cards.copy():
            del self.q.page[name]
            self.q.client.cards.remove(name)
