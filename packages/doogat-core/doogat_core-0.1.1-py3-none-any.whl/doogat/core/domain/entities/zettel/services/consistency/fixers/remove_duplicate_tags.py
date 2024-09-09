from doogat.core.domain.value_objects.zettel_data import ZettelData


def remove_duplicate_tags(zettel_data: ZettelData) -> None:
    if zettel_data.metadata.get("tags", None) is not None:
        zettel_data.metadata["tags"] = list(set(zettel_data.metadata["tags"]))
