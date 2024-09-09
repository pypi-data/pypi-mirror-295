from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from doogat.core.domain.value_objects.zettel_data import ZettelData


import re
from datetime import datetime


def migrate_loop_log(zettel_data: ZettelData) -> None:
    h1, top_level_content = zettel_data.sections[0]

    log_items, filtered_top_level_content = extract_log(top_level_content)
    log_content = ""
    task_status = " "
    for item in log_items:
        entry_date = item[0]
        log_content = (
            log_content
            + f"- [{task_status}] {entry_date.strftime("%Y-%m-%d %H:%M")} - {item[1]} => {item[2]}\n"
        )
        task_status = "x"
    zettel_data.sections[0] = (h1, "\n".join(filtered_top_level_content))

    if log_content:
        zettel_data.sections.append(("## Log", log_content))


def extract_log(content: str) -> tuple[list[tuple[datetime, str, str]], list[str]]:
    pattern: str = r"(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}) - (.+) => (.+)"
    matches: list[tuple[datetime, str, str]] = []
    unmatched_lines: list[str] = []

    for line in content.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            datetime_str, text_before, text_after = match.groups()
            datetime_obj = datetime.strptime(
                datetime_str,
                "%d.%m.%Y %H:%M",
            ).astimezone()
            matches.append((datetime_obj, text_before.strip(), text_after.strip()))
        elif line.strip():
            unmatched_lines.append(line.strip())

    return matches, unmatched_lines
