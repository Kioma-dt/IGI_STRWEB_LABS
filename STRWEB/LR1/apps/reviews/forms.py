from __future__ import annotations

from django import forms

from apps.reviews.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("product", "customer", "rating", "title", "body", "is_published")
        labels = {
            "product": "Товар",
            "customer": "Клиент",
            "rating": "Рейтинг",
            "title": "Заголовок отзыва",
            "body": "Текст отзыва",
            "is_published": "Опубликован",
        }
        widgets = {
            "body": forms.Textarea(attrs={"rows": 5}),
        }