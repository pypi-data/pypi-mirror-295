from abc import ABC, abstractmethod
from typing import Iterable, Optional


class MultiTenantCrudRepository[E, ID, TENANT_ID](ABC):

    @abstractmethod
    def count(self, tenant_id: TENANT_ID) -> int:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, entity: E, tenant_id: TENANT_ID) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_all(self, tenant_id: TENANT_ID) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_by_id(self, entity_id: ID, tenant_id: TENANT_ID) -> None:
        raise NotImplementedError()

    @abstractmethod
    def exists_by_id(self, entity_id: ID, tenant_id: TENANT_ID) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def save(self, entity: E, tenant_id: TENANT_ID) -> None:
        raise NotImplementedError()

    @abstractmethod
    def save_all(self, entities: Iterable[E], tenant_id: TENANT_ID) -> None:
        raise NotImplementedError()

    @abstractmethod
    def find_all(self, tenant_id: TENANT_ID) -> Iterable[E]:
        raise NotImplementedError()

    @abstractmethod
    def find_by_id(self, entity_id: ID, tenant_id: TENANT_ID) -> Optional[E]:
        raise NotImplementedError()

    @abstractmethod
    def update(self, entity: E, tenant_id: TENANT_ID) -> None:
        raise NotImplementedError()



