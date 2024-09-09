from doogat.core.domain.value_objects.zettel_data import ZettelData

DEFAULT_TYPE = "note"


def set_default_type(zettel_data: ZettelData) -> None:
    zettel_data.metadata["type"] = DEFAULT_TYPE
