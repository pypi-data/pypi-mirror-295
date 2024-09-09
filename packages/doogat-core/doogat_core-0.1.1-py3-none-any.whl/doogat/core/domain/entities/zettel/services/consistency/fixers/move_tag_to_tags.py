from doogat.core.domain.value_objects.zettel_data import ZettelData


def move_tag_to_tags(zettel_data: ZettelData) -> None:
    if zettel_data.metadata.get("tag", None) is not None:
        if zettel_data.metadata.get("tags", None) is None:
            zettel_data.metadata["tags"] = []

        if isinstance(zettel_data.metadata["tag"], str):
            zettel_data.metadata["tag"] = [zettel_data.metadata["tag"]]

        zettel_data.metadata["tags"].extend(zettel_data.metadata["tag"])

        del zettel_data.metadata["tag"]
