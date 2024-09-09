from doogat.core.domain.value_objects.zettel_data import ZettelData

DEFAULT_TITLE = "Unknown title"


def set_default_title(zettel_data: ZettelData) -> None:
    if (
        zettel_data.metadata.get("title", None) is None
        and getattr(zettel_data, "sections", None) is not None
    ):
        first_heading, _ = zettel_data.sections[0]

        if first_heading.startswith("# "):
            zettel_data.metadata["title"] = first_heading[2:]

    # Fallback to default title
    if zettel_data.metadata.get("title", None) is None:
        zettel_data.metadata["title"] = DEFAULT_TITLE
