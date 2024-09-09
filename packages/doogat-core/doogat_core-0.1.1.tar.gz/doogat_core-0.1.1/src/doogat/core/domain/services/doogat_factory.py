import doogat.core.domain.entities as doogat_entities
from buvis.pybase.formatting import StringOperator


class DoogatFactory:
    @staticmethod
    def create(zettel: doogat_entities.Zettel) -> doogat_entities.Zettel:
        zettel_type = getattr(zettel, "type", "")

        if zettel_type in ("note", ""):  # generic Zettel
            return zettel

        # try downcasting to more specific Zettel type
        class_name = StringOperator.camelize(zettel_type) + "Zettel"

        try:
            entity_class = getattr(doogat_entities, class_name)
        except AttributeError:
            return zettel
        else:
            downcasted_zettel = entity_class()
            downcasted_zettel.replace_data(zettel.get_data())
            return downcasted_zettel
