from django.conf import settings
from django.db import migrations


def fwd_create_user(apps, schema_editor) -> None:
    user_model = apps.get_model(settings.AUTH_USER_MODEL)
    user = user_model.objects.create_superuser(
        username="fguerin",
        email="fguerin@ville-tourcoing.fr",
    )


def rev_create_user(apps, schema_editor) -> None:
    pass


class Migration(migrations.Migration):
    initial = False
    dependencies = [
        ("example_app", "0001_initial"),
    ]
    operations = [
        migrations.RunPython(
            fwd_create_user,
            rev_create_user,
            atomic=True,
        )
    ]
