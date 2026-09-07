from __future__ import annotations

import re

from django import template

register = template.Library()


@register.filter
def tel_href(value: str) -> str:
    """Normalize phone for tel: URI (digits and leading + only)."""
    if not value:
        return ""
    cleaned = re.sub(r"[^\d+]", "", str(value))
    if cleaned.count("+") > 1:
        cleaned = cleaned.replace("+", "")
        cleaned = "+" + cleaned
    elif "+" in cleaned and not cleaned.startswith("+"):
        cleaned = cleaned.replace("+", "")
    return cleaned


@register.filter
def iso8601(value) -> str:
    """HTML5-safe datetime attribute (no >3 fractional second digits)."""
    if value is None:
        return ""
    try:
        return value.strftime("%Y-%m-%dT%H:%M:%S%z")
    except Exception:
        return str(value)
