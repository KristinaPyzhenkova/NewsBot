# Generated by Django 4.2 on 2024-01-04 17:10

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Channel",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата и время изменения"
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("type", models.CharField(max_length=250, verbose_name="type")),
                ("title", models.CharField(max_length=250, verbose_name="title")),
                (
                    "folder_url",
                    models.CharField(
                        blank=True, max_length=250, null=True, verbose_name="folder_url"
                    ),
                ),
                (
                    "slug",
                    models.CharField(
                        blank=True, max_length=250, null=True, verbose_name="slug"
                    ),
                ),
                ("chat_id", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "supergroup_id",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="supergroup_id",
                    ),
                ),
            ],
            options={
                "verbose_name": "Канал",
                "verbose_name_plural": "Каналы",
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата и время изменения"
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("media_album_id", models.CharField(max_length=50)),
                ("date", models.CharField(max_length=50)),
                ("interaction_info", models.TextField()),
                ("text", models.TextField()),
                ("type", models.CharField(max_length=50, verbose_name="type")),
                ("date_human", models.DateTimeField()),
                ("view_count", models.PositiveIntegerField(default=0)),
                ("forward_count", models.PositiveIntegerField(default=0)),
                ("reply_count", models.PositiveIntegerField(default=0)),
                ("reactions_info", models.TextField()),
                ("reactions_total_count", models.PositiveIntegerField(default=0)),
                ("positive_count", models.PositiveIntegerField(default=0)),
                ("negative_count", models.PositiveIntegerField(default=0)),
                ("neutral_count", models.PositiveIntegerField(default=0)),
                ("score", models.CharField(max_length=50, verbose_name="score")),
                ("message_id", models.CharField(max_length=50)),
                ("is_published", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
            },
        ),
        migrations.CreateModel(
            name="Setting",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата и время изменения"
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("value", models.TextField(blank=True, max_length=250, null=True)),
                ("number", models.IntegerField(blank=True, null=True)),
                ("boolean", models.IntegerField(default=True)),
                ("text", models.TextField(blank=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]