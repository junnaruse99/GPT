# Generated by Django 4.2.4 on 2023-08-08 03:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createdBy', models.UUIDField()),
                ('createdOn', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=500)),
                ('response', models.TextField()),
            ],
        ),
    ]