"""Utility functions for WhyHow resources."""


def flatten_tags(tags: dict[str, list[str]]) -> list[str]:
    """Flatten tags."""
    return [tag for tags_list in tags.values() for tag in tags_list]
