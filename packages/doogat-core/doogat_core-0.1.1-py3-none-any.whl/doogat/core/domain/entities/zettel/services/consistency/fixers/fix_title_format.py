from buvis.pybase.formatting import StringOperator

from doogat.core.domain.value_objects.zettel_data import ZettelData


def fix_title_format(zettel_data: ZettelData) -> None:
    zettel_data.metadata["title"] = StringOperator.replace_abbreviations(
        text=zettel_data.metadata["title"],
        level=0,
    )
