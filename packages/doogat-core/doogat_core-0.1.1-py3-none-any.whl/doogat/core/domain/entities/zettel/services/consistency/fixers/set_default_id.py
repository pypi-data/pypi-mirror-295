from datetime import timezone

from doogat.core.domain.value_objects.zettel_data import ZettelData


def set_default_id(zettel_data: ZettelData) -> None:
    id_str = (
        zettel_data.metadata["date"]
        .astimezone(timezone.utc)
        .strftime(
            "%Y%m%d%H%M%S",
        )
    )
    try:
        zettel_data.metadata["id"] = int(id_str)
    except ValueError as err:
        raise ValueError from err
