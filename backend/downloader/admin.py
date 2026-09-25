from django.contrib import admin
from .models import DownloadRequest

@admin.register(DownloadRequest)
class DownloadRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'video_title', 'quality', 'status', 'client_ip', 'created_at', 'completed_at')
    list_filter = ('status', 'quality', 'created_at')
    search_fields = ('id', 'video_title', 'source_url', 'client_ip', 'error_code')
    readonly_fields = ('id', 'created_at', 'completed_at')
