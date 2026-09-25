import uuid
from django.db import models

class DownloadRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_url = models.URLField(max_length=2048, help_text="Requested public video URL")
    video_title = models.CharField(max_length=500, blank=True, null=True)
    quality = models.CharField(max_length=50, default='best', help_text="Requested format or resolution")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )
    error_code = models.CharField(max_length=100, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    file_size_bytes = models.BigIntegerField(blank=True, null=True)
    client_ip = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Download Request'
        verbose_name_plural = 'Download Requests'

    def __str__(self):
        title = self.video_title or self.source_url[:30]
        return f"[{self.status.upper()}] {title} ({self.quality})"
