import pytest
from django.test import TestCase, Client
from django.urls import reverse
from downloader.models import DownloadRequest
from downloader.validators import validate_video_url
from downloader.utils import sanitize_filename, format_duration, format_filesize

class DownloaderApiTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health_check_endpoint(self):
        response = self.client.get(reverse('health_check'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'ok')
        self.assertIn('Django', data.get('framework', ''))

    def test_url_validation_ssrf_blocking(self):
        # Valid public URLs
        self.assertTrue(validate_video_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")[0])
        self.assertTrue(validate_video_url("https://vimeo.com/76979871")[0])

        # Blocked internal / private / SSRF targets
        self.assertFalse(validate_video_url("http://127.0.0.1/video.mp4")[0])
        self.assertFalse(validate_video_url("http://localhost:8000/video")[0])
        self.assertFalse(validate_video_url("http://192.168.1.1/video")[0])
        self.assertFalse(validate_video_url("http://10.0.0.1/video")[0])
        self.assertFalse(validate_video_url("http://169.254.169.254/latest/meta-data")[0])
        self.assertFalse(validate_video_url("file:///etc/passwd")[0])
        self.assertFalse(validate_video_url("")[0])

    def test_invalid_video_info_request(self):
        response = self.client.post(
            reverse('video_info'),
            data={"url": "http://127.0.0.1:8000/private"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get('error', {}).get('code'), 'INVALID_URL')

    def test_empty_video_info_request(self):
        response = self.client.post(
            reverse('video_info'),
            data={},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get('error', {}).get('code'), 'INVALID_URL')

    def test_filename_sanitization(self):
        # Path traversal protection
        cleaned = sanitize_filename("../../../secret_file.mp4")
        self.assertNotIn("..", cleaned)
        self.assertNotIn("/", cleaned)
        self.assertNotIn("\\", cleaned)

        # Windows reserved filenames
        self.assertTrue(sanitize_filename("CON.mp4").startswith("file_"))
        self.assertTrue(sanitize_filename("AUX.mp4").startswith("file_"))

    def test_formatting_helpers(self):
        self.assertEqual(format_duration(65), "1:05")
        self.assertEqual(format_duration(3665), "1:01:05")
        self.assertEqual(format_duration(0), "0:00")

        self.assertIn("MB", format_filesize(10 * 1024 * 1024))
        self.assertIn("KB", format_filesize(400 * 1024))

    def test_download_request_model(self):
        req = DownloadRequest.objects.create(
            source_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            quality="1080p",
            status=DownloadRequest.Status.PENDING,
            client_ip="127.0.0.1"
        )
        self.assertEqual(req.status, DownloadRequest.Status.PENDING)
        self.assertIn("PENDING", str(req))

    def test_js_runtimes_configuration(self):
        from downloader.services import get_discovered_js_runtimes, VideoService
        runtimes = get_discovered_js_runtimes()
        self.assertIsInstance(runtimes, dict)
        self.assertIn('deno', runtimes)
        self.assertIn('node', runtimes)

        opts = VideoService.get_ydl_opts()
        self.assertIn('js_runtimes', opts)
        self.assertTrue(opts.get('skip_download'))
        self.assertIn('extractor_args', opts)
        self.assertIn('youtube', opts['extractor_args'])


