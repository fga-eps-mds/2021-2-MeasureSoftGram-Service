import contextlib
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError


User = get_user_model()


class Command(BaseCommand):
    help = "Registra os dados iniciais da aplicação no banco de dados"

    def handle(self, *args, **options):
        with contextlib.suppress(IntegrityError):
            User.objects.create_superuser(
                username="admin",
                email="admin@admin.com",
                password="admin",
            )