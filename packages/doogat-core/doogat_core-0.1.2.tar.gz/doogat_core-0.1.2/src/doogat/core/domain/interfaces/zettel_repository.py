from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from doogat.core.domain.entities.zettel.zettel import Zettel


class ZettelRepository(ABC):
    @abstractmethod
    def save(self: ZettelRepository, zettel: Zettel) -> None:
        pass

    @abstractmethod
    def find_by_id(self: ZettelRepository, zettel_id: str) -> Zettel:
        pass

    @abstractmethod
    def find_all(self: ZettelRepository) -> list[Zettel]:
        pass

    @abstractmethod
    def find_by_location(self: ZettelRepository, repository_location: str) -> Zettel:
        pass
