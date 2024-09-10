from doogat.core.domain.value_objects.zettel_data import ZettelData


def sort_tags(zettel_data: ZettelData) -> None:
    if zettel_data.metadata.get("tags", None) is not None:
        zettel_data.metadata["tags"] = sorted(zettel_data.metadata["tags"])
