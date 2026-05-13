from __future__ import annotations

from django import forms

from apps.news.models import NewsArticle


class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ("title", "slug", "body", "published_at", "is_published")
        widgets = {
            "body": forms.Textarea(attrs={"rows": 10}),
            "published_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
