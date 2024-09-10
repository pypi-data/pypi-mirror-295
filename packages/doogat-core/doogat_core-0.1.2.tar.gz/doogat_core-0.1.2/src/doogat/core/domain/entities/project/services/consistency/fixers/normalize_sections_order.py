from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from doogat.core.domain.value_objects.zettel_data import ZettelData


def normalize_sections_order(zettel_data: ZettelData) -> None:
    reordered_sections = []
    for section in zettel_data.sections:
        if section[0].startswith("# "):
            reordered_sections.insert(0, (section[0], section[1]))
            continue
        if section[0] == "## Description":
            reordered_sections.insert(1, (section[0], section[1]))
            continue
        if section[0] == "## Log":
            reordered_sections.insert(2, (section[0], section[1]))
            continue
        if section[0] == "## Actions buffer":
            reordered_sections.insert(3, (section[0], section[1]))
            continue
        reordered_sections.append((section[0], section[1]))

    zettel_data.sections = reordered_sections
