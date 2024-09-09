from abc import ABC

from h2o_wave import Q


class ViewModel(ABC):

    def __init__(self, q: Q):
        self.q = q
