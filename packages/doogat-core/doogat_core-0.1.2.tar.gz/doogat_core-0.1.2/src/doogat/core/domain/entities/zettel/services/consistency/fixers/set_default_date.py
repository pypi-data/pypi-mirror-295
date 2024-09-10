from datetime import datetime, timezone

from doogat.core.domain.value_objects.zettel_data import ZettelData


def set_default_date(zettel_data: ZettelData) -> None:
    zettel_data.metadata["date"] = datetime.now(timezone.utc)
