# Generated by Django 5.2.2 on 2025-06-11 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cards", "0003_alter_cardprinting_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="cardprinting",
            unique_together={("unique_id",)},
        ),
    ]
