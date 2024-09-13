"""mirror submodule

Part of sopel-flipper.

Copyright 2024 dgw, technobabbl.es
"""
from __future__ import annotations

from . import data


def transform(text: str) -> str:
    """Mirror the input ``text`` as best as possible using exotic Unicode."""
    return ''.join(data.REPLACEMENTS.get(c, c) for c in text[::-1])
