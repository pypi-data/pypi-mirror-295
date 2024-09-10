from doogat.core.domain.entities.zettel.services.consistency.fixers.align_h1_to_title import (
    align_h1_to_title,
)
from doogat.core.domain.entities.zettel.services.consistency.fixers.fix_title_format import (
    fix_title_format,
)
from doogat.core.domain.entities.zettel.services.consistency.fixers.move_tag_to_tags import (
    move_tag_to_tags,
)
from doogat.core.domain.entities.zettel.services.consistency.fixers.move_zkn_id_to_id import (
    move_zkn_id_to_id,
)
from doogat.core.domain.entities.zettel.services.consistency.fixers.normalize_type import (
    normalize_type,
)
from doogat.core.domain.entities.zettel.services.consistency.fixers.remove_duplicate_tags import (
    remove_duplicate_tags,
)
from doogat.core.domain.entities.zettel.services.consistency.fixers.set_default_date import (
    set_default_date,
)
from doogat.core.domain.entities.zettel.services.consistency.fixers.set_default_id import (
    set_default_id,
)
from doogat.core.domain.entities.zettel.services.consistency.fixers.set_default_processed import (
    set_default_processed,
)
from doogat.core.domain.entities.zettel.services.consistency.fixers.set_default_publish import (
    set_default_publish,
)
from doogat.core.domain.entities.zettel.services.consistency.fixers.set_default_tags import (
    set_default_tags,
)
from doogat.core.domain.entities.zettel.services.consistency.fixers.set_default_title import (
    set_default_title,
)
from doogat.core.domain.entities.zettel.services.consistency.fixers.set_default_type import (
    set_default_type,
)
from doogat.core.domain.entities.zettel.services.consistency.fixers.sort_tags import (
    sort_tags,
)
from doogat.core.domain.value_objects.zettel_data import ZettelData


class ZettelConsistencyService:
    @staticmethod
    def set_missing_defaults(zettel_data: ZettelData) -> None:
        if zettel_data.metadata.get("date", None) is None:
            set_default_date(zettel_data)

        if zettel_data.metadata.get("id", None) is None:
            set_default_id(zettel_data)

        if zettel_data.metadata.get("title", None) is None:
            set_default_title(zettel_data)

        if zettel_data.metadata.get("type", None) is None:
            set_default_type(zettel_data)

        if zettel_data.metadata.get("tags", None) is None:
            set_default_tags(zettel_data)

        if zettel_data.metadata.get("publish", None) is None:
            set_default_publish(zettel_data)

        if zettel_data.metadata.get("processed", None) is None:
            set_default_processed(zettel_data)

    @staticmethod
    def ensure_consistency(zettel_data: ZettelData) -> None:
        move_zkn_id_to_id(zettel_data)
        normalize_type(zettel_data)
        ZettelConsistencyService.set_missing_defaults(zettel_data)
        move_tag_to_tags(zettel_data)
        remove_duplicate_tags(zettel_data)
        sort_tags(zettel_data)
        fix_title_format(zettel_data)
        align_h1_to_title(zettel_data)
