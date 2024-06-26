# Generated by Django 4.2 on 2024-02-17 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0002_remove_message_date_human_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения')),
                ('name', models.CharField(blank=True, choices=[('доллар', 'доллар'), ('евро', 'евро'), ('юань', 'юань'), ('BTC', 'BTC'), ('ETH', 'ETH')], default='доллар', max_length=12, null=True)),
                ('value', models.FloatField(blank=True, null=True)),
                ('exchange', models.CharField(blank=True, choices=[('currency', 'currency'), ('crypto', 'crypto')], default='currency', max_length=12, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
