import os
import logging
from pathlib import Path
from django.utils import timezone
from django.http import StreamingHttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import DownloadRequest
from .serializers import (
    VideoInfoRequestSerializer,
    VideoInfoResponseSerializer,
    DownloadRequestSerializer,
)
from .services import VideoService, DownloadService
from .utils import get_client_ip, cleanup_path

logger = logging.getLogger(__name__)

class HealthCheckView(APIView):
    """
    Health check endpoint for deployment verification.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({
            "status": "ok",
            "app": "Velora Video Downloader",
            "framework": "Django + Django REST Framework",
            "version": "1.0.0"
        })


class VideoInfoView(APIView):
    """
    Extracts video metadata and curated downloadable formats.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = VideoInfoRequestSerializer(data=request.data)
        if not serializer.is_valid():
            first_err = list(serializer.errors.values())[0]
            err_msg = first_err[0] if isinstance(first_err, list) else str(first_err)
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": "INVALID_URL",
                        "message": err_msg
                    }
                },
                status=status.HTTP_200_OK
            )

        url = serializer.validated_data['url']

        try:
            video_info = VideoService.extract_info(url)
            return Response({
                "success": True,
                "data": video_info
            })
        except ValueError as e:
            msg = str(e)
            code = "EXTRACTION_FAILED"
            if ":" in msg:
                parts = msg.split(":", 1)
                code = parts[0].strip()
                msg = parts[1].strip()
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": code,
                        "message": msg
                    }
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error in VideoInfoView: {e}", exc_info=True)
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": "SERVER_ERROR",
                        "message": "Unable to process video information. Please try again later."
                    }
                },
                status=status.HTTP_200_OK
            )


class VideoDownloadView(APIView):
    """
    Processes video stream download and streams the resulting file directly to browser.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = DownloadRequestSerializer(data=request.data)
        if not serializer.is_valid():
            first_err = list(serializer.errors.values())[0]
            err_msg = first_err[0] if isinstance(first_err, list) else str(first_err)
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": "INVALID_REQUEST",
                        "message": err_msg
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        url = serializer.validated_data['url']
        format_id = serializer.validated_data.get('format_id') or serializer.validated_data.get('quality') or 'best'
        client_ip = get_client_ip(request)

        # Create monitoring record in database
        download_record = DownloadRequest.objects.create(
            source_url=url,
            quality=format_id,
            status=DownloadRequest.Status.PROCESSING,
            client_ip=client_ip
        )

        try:
            file_path, filename, content_type, file_size = DownloadService.download_video(url, format_id)

            download_record.status = DownloadRequest.Status.COMPLETED
            download_record.file_size_bytes = file_size
            download_record.completed_at = timezone.now()
            download_record.save(update_fields=['status', 'file_size_bytes', 'completed_at'])

            def file_iterator_with_cleanup(filepath: Path, chunk_size: int = 65536):
                try:
                    with open(filepath, 'rb') as f:
                        while True:
                            chunk = f.read(chunk_size)
                            if not chunk:
                                break
                            yield chunk
                finally:
                    # Clean up temporary task folder after stream finishes
                    task_dir = filepath.parent
                    cleanup_path(task_dir)

            response = StreamingHttpResponse(
                file_iterator_with_cleanup(file_path),
                content_type=content_type
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Content-Length'] = str(file_size)
            response['Accept-Ranges'] = 'bytes'
            return response

        except ValueError as e:
            msg = str(e)
            code = "DOWNLOAD_FAILED"
            if ":" in msg:
                parts = msg.split(":", 1)
                code = parts[0].strip()
                msg = parts[1].strip()

            download_record.status = DownloadRequest.Status.FAILED
            download_record.error_code = code
            download_record.error_message = msg
            download_record.save(update_fields=['status', 'error_code', 'error_message'])

            return Response(
                {
                    "success": False,
                    "error": {
                        "code": code,
                        "message": msg
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Download processing failed: {e}", exc_info=True)
            download_record.status = DownloadRequest.Status.FAILED
            download_record.error_code = "SERVER_ERROR"
            download_record.error_message = str(e)
            download_record.save(update_fields=['status', 'error_code', 'error_message'])

            return Response(
                {
                    "success": False,
                    "error": {
                        "code": "SERVER_ERROR",
                        "message": "Failed to prepare video download. Please try again."
                    }
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
