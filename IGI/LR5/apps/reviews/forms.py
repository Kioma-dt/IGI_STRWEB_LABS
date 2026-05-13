from __future__ import annotations

from django import forms

from apps.reviews.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("product", "customer", "rating", "title", "body", "is_published")
        widgets = {
            "body": forms.Textarea(attrs={"rows": 5}),
        }
