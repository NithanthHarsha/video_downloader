from rest_framework import serializers
from .validators import validate_video_url

class VideoInfoRequestSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=2048, required=True)

    def validate_url(self, value):
        is_valid, error_msg = validate_video_url(value)
        if not is_valid:
            raise serializers.ValidationError(error_msg or "Please enter a valid video URL.")
        return value.strip()

class VideoFormatSerializer(serializers.Serializer):
    format_id = serializers.CharField()
    quality = serializers.CharField()
    ext = serializers.CharField(default="mp4")
    resolution = serializers.CharField(allow_null=True, required=False)
    filesize_approx = serializers.IntegerField(allow_null=True, required=False)
    filesize_str = serializers.CharField(allow_null=True, required=False)
    has_video = serializers.BooleanField(default=True)
    has_audio = serializers.BooleanField(default=True)
    is_recommended = serializers.BooleanField(default=False)
    vcodec = serializers.CharField(allow_null=True, required=False)
    acodec = serializers.CharField(allow_null=True, required=False)

class VideoInfoResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    url = serializers.CharField()
    title = serializers.CharField()
    thumbnail = serializers.CharField(allow_null=True, required=False)
    duration = serializers.IntegerField(allow_null=True, required=False)
    duration_str = serializers.CharField(allow_null=True, required=False)
    uploader = serializers.CharField(allow_null=True, required=False)
    uploader_url = serializers.CharField(allow_null=True, required=False)
    view_count = serializers.IntegerField(allow_null=True, required=False)
    description = serializers.CharField(allow_null=True, required=False)
    formats = VideoFormatSerializer(many=True)

class DownloadRequestSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=2048, required=True)
    quality = serializers.CharField(max_length=50, default="best", required=False)
    format_id = serializers.CharField(max_length=50, default="best", required=False)

    def validate_url(self, value):
        is_valid, error_msg = validate_video_url(value)
        if not is_valid:
            raise serializers.ValidationError(error_msg or "Please enter a valid video URL.")
        return value.strip()
