from doogat.core.domain.value_objects.zettel_data import ZettelData


def set_default_processed(zettel_data: ZettelData) -> None:
    zettel_data.metadata["processed"] = False
