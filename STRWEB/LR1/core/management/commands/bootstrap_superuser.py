from __future__ import annotations

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = (
        "Создаёт суперпользователя из переменных окружения, если его ещё нет. "
        "Переменные: BOOTSTRAP_SUPERUSER_USERNAME (по умолчанию admin), "
        "BOOTSTRAP_SUPERUSER_EMAIL, BOOTSTRAP_SUPERUSER_PASSWORD (обязательна)."
    )

    def handle(self, *args, **options) -> None:
        username = os.environ.get("BOOTSTRAP_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("BOOTSTRAP_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("BOOTSTRAP_SUPERUSER_PASSWORD")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"User {username!r} already exists; skip."))
            return

        if not password:
            self.stderr.write(
                "Set BOOTSTRAP_SUPERUSER_PASSWORD in the environment to create a superuser.",
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS(f"Superuser {username!r} created."))
