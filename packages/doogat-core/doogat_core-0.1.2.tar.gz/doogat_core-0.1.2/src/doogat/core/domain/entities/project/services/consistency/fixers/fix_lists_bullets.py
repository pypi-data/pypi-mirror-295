from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from doogat.core.domain.value_objects.zettel_data import ZettelData


def fix_lists_bullets(zettel_data: ZettelData) -> None:
    """
    Replaces asterisk (*) bullets with hyphen (-) bullets in the content of ZettelData sections.

    :param zettel_data: The input ZettelData object whose sections need to be processed.
    :type zettel_data: ZettelData

    :return: None (modifies the input zettel_data object in-place)

    :note: This function assumes that the input ZettelData object has a 'sections' attribute,
           which is a list of tuples containing section metadata and content.
    """
    fixed_sections = []
    for section in zettel_data.sections:
        section_content_reformatted = []

        for line in section[1].split("\n"):
            if line.startswith("* "):
                section_content_reformatted.append(f"- {line[2:].strip()}")
            else:
                section_content_reformatted.append(line.strip())
        fixed_sections.append((section[0], "\n".join(section_content_reformatted)))

    zettel_data.sections = fixed_sections
