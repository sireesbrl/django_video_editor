from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    original_video = models.FileField(upload_to='videos/')
    original_audio = models.FileField(upload_to='audio/', blank=True, null=True)  # Optional audio field
    processed_video = models.CharField(max_length=255, blank=True, null=True)  # Path to processed video
    text_content = models.CharField(max_length=255, blank=True, null=True)  # Text content for overlay
    text_position = models.CharField(max_length=255, blank=True, null=True, default="center,center")  # Position of text

    def __str__(self):
        return self.title
