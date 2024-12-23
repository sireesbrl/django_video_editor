# Generated by Django 5.1.4 on 2024-12-23 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("video_editor", "0002_alter_video_processed_video"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="original_audio",
            field=models.FileField(blank=True, null=True, upload_to="audio/"),
        ),
        migrations.AddField(
            model_name="video",
            name="text_content",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="video",
            name="text_position",
            field=models.CharField(
                blank=True, default="center,center", max_length=255, null=True
            ),
        ),
    ]
