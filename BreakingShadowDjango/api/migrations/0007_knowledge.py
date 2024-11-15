# Generated by Django 4.2.16 on 2024-11-12 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('api', '0006_expert_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Knowledge',
            fields=[
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/knowledge/')),
                ('short_description', models.CharField(blank=True, max_length=255, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user_w_knowledge', serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
