from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime

from doogat.core.domain.entities.zettel.services.consistency.zettel_consistency_service import (
    ZettelConsistencyService,
)
from doogat.core.domain.value_objects.zettel_data import ZettelData


class Zettel:
    def __init__(self: Zettel, zettel_data: ZettelData | None = None) -> None:
        self._data = ZettelData()

        if zettel_data:
            self.replace_data(zettel_data)

    def get_data(self: Zettel) -> ZettelData:
        return self._data

    def replace_data(self: Zettel, zettel_data: ZettelData) -> None:
        self._data = zettel_data
        self._ensure_consistency()
        self._alias_attributes()

    def _ensure_consistency(self: Zettel) -> None:
        ZettelConsistencyService.ensure_consistency(self._data)

    def _alias_attributes(self: Zettel) -> None:
        for key, value in {
            **self._data.metadata,
            **self._data.reference,
        }.items():
            setattr(self, key, value)

    @property
    def id(self: Zettel) -> int | None:
        if self._data.metadata.get("id", None) is None:
            return None
        try:
            return int(self._data.metadata["id"])
        except ValueError:
            return None

    @id.setter
    def id(self: Zettel, value: int) -> None:
        try:
            self._data.metadata["id"] = int(value)
        except ValueError as err:
            raise ValueError from err
        self._ensure_consistency()

    @property
    def title(self: Zettel) -> str | None:
        if self._data.metadata.get("title", None) is None:
            return None

        return str(self._data.metadata["title"])

    @title.setter
    def title(self: Zettel, value: str) -> None:
        self._data.metadata["title"] = str(value)
        self._ensure_consistency()

    @property
    def date(self: Zettel) -> datetime | None:
        if self._data.metadata.get("date", None) is None:
            return None

        return self._data.metadata["date"]

    @date.setter
    def date(self: Zettel, value: datetime) -> None:
        self._data.metadata["date"] = value
        self._ensure_consistency()

    @property
    def type(self: Zettel) -> str | None:
        if self._data.metadata.get("type", None) is None:
            return None

        return str(self._data.metadata["type"])

    @type.setter
    def type(self: Zettel, value: str) -> None:
        self._data.metadata["type"] = str(value)
        self._ensure_consistency()

    @property
    def tags(self: Zettel) -> list | None:
        if self._data.metadata.get("tags", None) is None:
            return None
        return self._data.metadata["tags"]

    @tags.setter
    def tags(self: Zettel, value: list[str]) -> None:
        if not isinstance(value, list):
            value = [value]

        self._data.metadata["tags"] = value
        self._ensure_consistency()

    @property
    def publish(self: Zettel) -> bool:
        if self._data.metadata.get("publish", None) is None:
            return False
        return self._data.metadata["publish"]

    @publish.setter
    def publish(self: Zettel, value: bool) -> None:
        if value:
            self._data.metadata["publish"] = True
        else:
            self._data.metadata["publish"] = False
        self._ensure_consistency()

    @property
    def processed(self: Zettel) -> bool:
        if self._data.metadata.get("processed", None) is None:
            return False
        return self._data.metadata["processed"]

    @processed.setter
    def processed(self: Zettel, value: bool) -> None:
        if value:
            self._data.metadata["processed"] = True
        else:
            self._data.metadata["processed"] = False
        self._ensure_consistency()
