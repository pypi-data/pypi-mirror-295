from abc import ABC, abstractmethod
from enum import Enum
from typing import Union, List

from h2o_wave import Q, SidePanel, Dialog, Component, NotificationBar


class OverlayType(Enum):
    SIDE_PANEL = "side_panel"
    DIALOG = "dialog"
    NOTIFICATION_BAR = "notification_bar"


class Overlay(ABC):

    def __init__(self, q: Q):
        self.q = q

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def overlay_type(self) -> OverlayType:
        pass

    @abstractmethod
    def render(self) -> Union[SidePanel, Dialog, NotificationBar]:
        pass

    @abstractmethod
    def items(self) -> List[Component]:
        pass

    async def show(self):
        overlay = self.render()
        overlay.name = self.name()
        overlay.events = ['dismissed']

        self.q.page['meta'][self.overlay_type().value] = overlay
        await self.q.page.save()

    @classmethod
    async def rebuild(cls, q: Q):
        self = cls(q)
        self.q.page['meta'][self.overlay_type().value].items = self.items()
        await self.q.page.save()

    @classmethod
    async def close(cls, q: Q, ignore_on_close: bool = False):
        self = cls(q)
        if not ignore_on_close:
            await self.on_close()
        self.q.page['meta'][self.overlay_type().value] = None
        await self.q.page.save()

    @abstractmethod
    async def on_close(self):
        pass
