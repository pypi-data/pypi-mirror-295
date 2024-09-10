from doogat.core.domain.value_objects.zettel_data import ZettelData

TYPE_MIGRATIONS = {
    "loop": "project",
    "wiki-article": "note",
    "zettel": "note",
}


def normalize_type(zettel_data: ZettelData) -> None:
    if zettel_data.metadata["type"] in TYPE_MIGRATIONS:
        zettel_data.metadata["type"] = TYPE_MIGRATIONS[zettel_data.metadata["type"]]
