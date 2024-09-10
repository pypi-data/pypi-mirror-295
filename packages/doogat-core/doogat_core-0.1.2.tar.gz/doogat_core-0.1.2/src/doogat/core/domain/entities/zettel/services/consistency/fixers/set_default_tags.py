from doogat.core.domain.value_objects.zettel_data import ZettelData


def set_default_tags(zettel_data: ZettelData) -> None:
    zettel_data.metadata["tags"] = []
