from abc import ABC, abstractmethod
from typing import Iterable, Optional


class CrudRepository[E, ID](ABC):

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, entity: E) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_all(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_by_id(self, entity_id: ID) -> None:
        raise NotImplementedError()

    @abstractmethod
    def exists_by_id(self, entity_id: ID) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def save(self, entity: E) -> None:
        raise NotImplementedError()

    @abstractmethod
    def save_all(self, entities: Iterable[E]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def find_all(self) -> Iterable[E]:
        raise NotImplementedError()

    @abstractmethod
    def find_by_id(self, entity_id: ID) -> Optional[E]:
        raise NotImplementedError()

    @abstractmethod
    def update(self, entity: E) -> None:
        raise NotImplementedError()



