from doogat.core.domain.entities.project.services.consistency.fixers.fix_lists_bullets import (
    fix_lists_bullets,
)
from doogat.core.domain.entities.project.services.consistency.fixers.migrate_loop_log import (
    migrate_loop_log,
)
from doogat.core.domain.entities.project.services.consistency.fixers.normalize_sections_order import (
    normalize_sections_order,
)
from doogat.core.domain.value_objects.zettel_data import ZettelData


class ProjectZettelConsistencyService:
    @staticmethod
    def ensure_consistency(zettel_data: ZettelData) -> None:
        fix_lists_bullets(zettel_data)
        migrate_loop_log(zettel_data)
        normalize_sections_order(zettel_data)
