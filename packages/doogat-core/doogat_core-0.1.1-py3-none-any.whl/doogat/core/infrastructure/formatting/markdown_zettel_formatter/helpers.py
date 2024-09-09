import re
from datetime import datetime

import yaml


def process_metadata(metadata: dict, first_keys: tuple) -> dict:
    """Process and return the full metadata with required keys first, followed by others."""
    return {
        **{key: metadata[key] for key in first_keys if key in metadata},
        **{k: v for k, v in sorted(metadata.items()) if k not in first_keys},
    }


def convert_datetimes(full_metadata: dict) -> list:
    """Convert datetime objects to formatted strings and return keys that were converted."""
    datetime_keys = [
        key for key in full_metadata if isinstance(full_metadata[key], datetime)
    ]
    for key in datetime_keys:
        full_metadata[key] = (
            full_metadata[key].astimezone().replace(microsecond=0).isoformat()
        )
    return datetime_keys


def metadata_to_yaml(full_metadata: dict, datetime_keys: list) -> str:
    """Convert metadata dictionary to a YAML-formatted string."""
    metadata_str = yaml.dump(
        full_metadata,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
    ).strip()
    datetime_regex = re.compile(
        r"^({})'([^']*)'(.*)$".format("|".join(datetime_keys)),
        flags=re.MULTILINE,
    )
    return datetime_regex.sub(r"\1\2\3", metadata_str)


def remove_quotes_in_datetime_keys(metadata_str: str, datetime_keys: list) -> str:
    # Remove quotes in datetime keys
    for key in datetime_keys:
        pattern = rf"^({key}[^']*)'([^']*)'(.*)$"
        return re.sub(
            pattern,
            r"\g<1>\g<2>\g<3>",
            metadata_str,
            flags=re.MULTILINE,
        )
    return metadata_str


def format_metadata(metadata: dict, first_keys: tuple) -> str:
    full_metadata = process_metadata(
        metadata,
        first_keys,
    )
    datetime_keys = convert_datetimes(full_metadata)
    metadata_str = metadata_to_yaml(
        full_metadata,
        datetime_keys,
    )
    return remove_quotes_in_datetime_keys(
        metadata_str,
        datetime_keys,
    )


def format_reference(reference: dict) -> str:
    return "\n".join(f"{k}:: {v.lstrip()}" for k, v in reference.items())


def format_sections(sections: list) -> str:
    return "\n".join(
        f"\n{heading}\n\n{content.strip()}" if content.strip() else f"\n{heading}"
        for heading, content in sections
    )
