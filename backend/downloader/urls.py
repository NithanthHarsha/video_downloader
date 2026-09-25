from django.urls import path
from .views import HealthCheckView, VideoInfoView, VideoDownloadView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health_check'),
    path('video/info/', VideoInfoView.as_view(), name='video_info'),
    path('video/download/', VideoDownloadView.as_view(), name='video_download'),
]
