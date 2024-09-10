from doogat.core.domain.value_objects.zettel_data import ZettelData


def align_h1_to_title(zettel_data: ZettelData) -> None:
    title_heading = f"# {zettel_data.metadata["title"]}"

    if len(zettel_data.sections) > 0:
        first_heading, content = zettel_data.sections[0]
    else:
        first_heading = ""
        content = ""

    if first_heading != title_heading:
        if first_heading != "" and not first_heading.startswith("# "):
            zettel_data.sections.insert(0, (title_heading, ""))
        elif first_heading == "" or first_heading.startswith("# "):
            zettel_data.sections[0] = (title_heading, content)
