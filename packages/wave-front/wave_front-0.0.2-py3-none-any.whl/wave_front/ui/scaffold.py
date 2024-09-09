from abc import ABC, abstractmethod
from typing import List

from h2o_wave import Zone, MetaCard, Q


class Scaffold(ABC):

    def __init__(self, q: Q):
        self.q = q

    # @staticmethod
    @abstractmethod
    def meta_card(self, page_zones: List[Zone]) -> MetaCard:
        pass
