# Generated by Django 5.2.2 on 2025-06-11 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cards", "0004_alter_cardprinting_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="cardprinting",
            name="flavour_text",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
