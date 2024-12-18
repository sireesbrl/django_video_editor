from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    original_video = models.FileField(upload_to='videos/')
    processed_video = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title
