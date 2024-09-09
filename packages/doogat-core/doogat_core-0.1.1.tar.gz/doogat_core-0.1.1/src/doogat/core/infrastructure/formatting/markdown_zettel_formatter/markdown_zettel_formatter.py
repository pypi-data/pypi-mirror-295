from doogat.core.domain.interfaces.zettel_formatter import ZettelFormatter
from doogat.core.domain.value_objects.zettel_data import ZettelData
from doogat.core.infrastructure.formatting.markdown_zettel_formatter.helpers import (
    format_metadata,
    format_reference,
    format_sections,
)


class MarkdownZettelFormatter(ZettelFormatter):
    TOP_KEYS: tuple = ("id", "title", "date", "type", "tags", "publish", "processed")

    @staticmethod
    def format(zettel_data: ZettelData) -> str:
        metadata_str = format_metadata(
            zettel_data.metadata,
            MarkdownZettelFormatter.TOP_KEYS,
        )
        reference_str = format_reference(zettel_data.reference)
        sections_str = format_sections(zettel_data.sections)

        return (
            f"---\n{metadata_str}\n---\n{sections_str}\n\n---\n{reference_str}"
        ).rstrip()
