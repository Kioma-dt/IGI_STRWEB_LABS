from __future__ import annotations

import re
from datetime import date, timedelta

from django.core.exceptions import ValidationError

_PHONE_RE = re.compile(r"^\+375 \(29\) \d{3}-\d{2}-\d{2}$")


def validate_phone_by_format_375_29(value: str) -> None:
    if not _PHONE_RE.match(value):
        raise ValidationError(
            "Invalid phone format. Expected: +375 (29) XXX-XX-XX.",
        )


def validate_age_18_plus(birth_date: date) -> None:
    if birth_date is None:
        return
    today = date.today()
    min_allowed = today - timedelta(days=18 * 365)
    if birth_date > min_allowed:
        raise ValidationError("Customer must be 18 years or older.")
