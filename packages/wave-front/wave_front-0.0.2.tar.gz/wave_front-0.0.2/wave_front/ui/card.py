from abc import ABC, abstractmethod
from typing import List, Union, Callable

from h2o_wave import Q, Component, Command, Data, NavGroup, Breadcrumb


class Card(ABC):

    def __init__(self, q: Q, persist: bool = False):
        self.q = q
        self.persist = persist

    @classmethod
    def name(cls) -> str:
        return f"{cls.__name__}Card"

    @abstractmethod
    def build(self) -> object:
        pass

    @abstractmethod
    def items(self) -> Union[List[Component], List[Breadcrumb], List[Command], List[NavGroup], Union[Data, str]]:
        pass

    @classmethod
    async def rebuild(cls, q: Q, batched: bool = False, whole_card: bool = False):
        self = cls(q)

        if whole_card:
            self.q.page[self.name()] = self.build()
        else:
            for key, func in self.rebuild_fields():
                self.q.page[self.name()][key] = func()

        if not batched:
            await self.q.page.save()

    def rebuild_fields(self) -> list[(str, Callable)]:
        return [
            ("items", self.items),
        ]

    def register_card(self):
        if not self.persist:
            self.q.client.cards.add(self.name())

    def show(self):
        self.register_card()
        self.q.page[self.name()] = self.build()


async def batch_rebuild(q: Q, cards: List[Card], whole_card: bool = False):
    for card in cards:
        await card.rebuild(q, batched=True, whole_card=whole_card)

    await q.page.save()
