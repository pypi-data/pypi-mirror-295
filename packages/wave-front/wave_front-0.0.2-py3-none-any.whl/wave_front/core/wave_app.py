from abc import ABC, abstractmethod
from typing import List

from h2o_wave import Q, run_on

from ..ui.app_page import AppPage
from ..ui.card import Card
from ..utils import redirect_to


class WaveApp(ABC):

    def __init__(self, q: Q):
        self.q = q

    @classmethod
    async def run(cls, q: Q):
        self = cls(q)

        await self._initialize()

        if not await run_on(q):
            if q.args['#'] is None:
                await self._on_home()

            # await skip_loading(q)

        for card in self.persistent_cards():
            await card.rebuild(self.q, batched=True)

        await q.page.save()

    async def _on_home(self):
        self.default_page()
        for card in self.persistent_cards():
            await card.rebuild(self.q, batched=True)
        await redirect_to(self.q, self.initial_route())

    async def _initialize(self):
        await self._app_initialize()
        await self._user_initialize()
        await self._client_initialize()
        return self

    async def _app_initialize(self):
        if self.q.app.initialized:
            return

        self.q.app.initialized = True
        await self.load_assets()
        await self.app_init(self.q.app)

    async def _user_initialize(self):
        if self.q.user.initialized:
            return

        self.q.user.initialized = True
        await self.user_init(self.q.user, self.q.app)

    async def _client_initialize(self):
        if self.q.client.initialized:
            return

        self.q.client.initialized = True

        await self.client_init(self.q.client, self.q.user, self.q.app)

        self.q.client.theme = self.initial_theme()
        self.q.client.cards = set()

        for card in self.persistent_cards():
            card.persist = True
            card.show()

    @abstractmethod
    async def app_init(self, app):
        pass

    @abstractmethod
    async def user_init(self, user, app):
        pass

    @abstractmethod
    async def client_init(self, client, user, app):
        pass

    @abstractmethod
    async def load_assets(self):
        pass

    @abstractmethod
    def persistent_cards(self) -> List[Card]:
        pass

    @abstractmethod
    def default_page(self) -> AppPage:
        pass

    @abstractmethod
    def initial_route(self) -> str:
        pass

    @abstractmethod
    def initial_theme(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def on_startup():
        pass

    @staticmethod
    @abstractmethod
    def on_shutdown():
        pass
