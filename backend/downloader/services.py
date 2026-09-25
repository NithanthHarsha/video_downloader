import os
import uuid
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import yt_dlp
from django.conf import settings
from .utils import sanitize_filename, format_duration, format_filesize

logger = logging.getLogger(__name__)

class VideoService:
    """
    Handles extracting video metadata and determining available formats
    using yt-dlp in a safe, lawful manner.
    """

    @staticmethod
    def get_ydl_opts() -> Dict[str, Any]:
        return {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'extract_flat': False,
            'noplaylist': True,
            'socket_timeout': 30,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Sec-Fetch-Mode': 'navigate',
            }
        }

    @classmethod
    def extract_info(cls, url: str) -> Dict[str, Any]:
        """
        Extracts video metadata from a public URL.
        """
        ydl_opts = cls.get_ydl_opts()

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    raise ValueError("NO_DATA: No metadata returned for this video.")

                if 'entries' in info and info['entries']:
                    info = info['entries'][0]

                return cls._parse_video_info(url, info)

        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e).lower()
            logger.warning(f"yt-dlp DownloadError for {url}: {error_msg}")

            if "private video" in error_msg or "is private" in error_msg:
                raise ValueError("PRIVATE_VIDEO: This video is private and cannot be accessed.")
            elif "drm" in error_msg or "protected" in error_msg:
                raise ValueError("DRM_PROTECTED: This video is DRM-protected and cannot be downloaded.")
            elif "sign in" in error_msg or "login" in error_msg or "members-only" in error_msg:
                raise ValueError("RESTRICTED_CONTENT: This video requires account authentication or membership.")
            elif "not available" in error_msg or "not found" in error_msg or "404" in error_msg:
                raise ValueError("VIDEO_NOT_FOUND: The requested video could not be found or is unavailable.")
            elif "geo" in error_msg or "country" in error_msg or "blocked" in error_msg:
                raise ValueError("GEO_RESTRICTED: This video is restricted in the server region.")
            elif "unsupported url" in error_msg:
                raise ValueError("UNSUPPORTED_URL: The provided URL is not supported.")
            else:
                raise ValueError(f"EXTRACTION_FAILED: Unable to process video. Please check the URL.")

        except Exception as e:
            logger.error(f"Unexpected error extracting {url}: {e}")
            raise ValueError(f"EXTRACTION_FAILED: {str(e)}")

    @classmethod
    def _parse_video_info(cls, url: str, info: Dict[str, Any]) -> Dict[str, Any]:
        raw_formats = info.get('formats', [])
        duration = info.get('duration')
        
        formats = cls._curate_formats(raw_formats, duration)

        if not formats:
            formats.append({
                "format_id": "best",
                "quality": "Best Available Quality",
                "ext": "mp4",
                "has_video": True,
                "has_audio": True,
                "is_recommended": True
            })

        return {
            "id": str(info.get('id', 'unknown')),
            "url": url,
            "title": info.get('title', 'Untitled Video'),
            "thumbnail": info.get('thumbnail'),
            "duration": duration,
            "duration_str": format_duration(duration),
            "uploader": info.get('uploader') or info.get('channel') or info.get('creator') or "Unknown Creator",
            "uploader_url": info.get('uploader_url') or info.get('channel_url'),
            "view_count": info.get('view_count'),
            "description": info.get('description', '')[:300] if info.get('description') else None,
            "formats": formats
        }

    @classmethod
    def _curate_formats(cls, raw_formats: List[Dict[str, Any]], duration: Optional[int | float]) -> List[Dict[str, Any]]:
        formats_by_height: Dict[int, Dict[str, Any]] = {}
        has_any_audio = False
        best_audio_format = None

        for f in raw_formats:
            vcodec = f.get('vcodec')
            acodec = f.get('acodec')
            height = f.get('height')
            ext = f.get('ext', 'mp4')

            is_video = vcodec and vcodec != 'none'
            is_audio = acodec and acodec != 'none'

            if is_audio and not is_video:
                has_any_audio = True
                if not best_audio_format or (f.get('tbr') or 0) > (best_audio_format.get('tbr') or 0):
                    best_audio_format = f

            if is_video and height:
                rounded_height = int(height)
                if rounded_height not in formats_by_height:
                    formats_by_height[rounded_height] = f
                else:
                    current = formats_by_height[rounded_height]
                    if ext == 'mp4' and current.get('ext') != 'mp4':
                        formats_by_height[rounded_height] = f
                    elif (f.get('tbr') or 0) > (current.get('tbr') or 0):
                        formats_by_height[rounded_height] = f

        curated: List[Dict[str, Any]] = []

        quality_labels = {
            2160: "4K (2160p)",
            1440: "2K (1440p)",
            1080: "1080p Full HD",
            720: "720p HD",
            480: "480p SD",
            360: "360p",
            240: "240p",
            144: "144p",
        }

        # Recommended / Best Available format
        curated.append({
            "format_id": "best",
            "quality": "Best Available Quality",
            "ext": "mp4",
            "has_video": True,
            "has_audio": True,
            "is_recommended": True,
            "resolution": None,
            "filesize_approx": None,
            "filesize_str": None,
        })

        sorted_heights = sorted(formats_by_height.keys(), reverse=True)

        for h in sorted_heights:
            if h < 240:
                continue
            fmt = formats_by_height[h]
            label = quality_labels.get(h, f"{h}p")
            
            filesize = fmt.get('filesize') or fmt.get('filesize_approx')
            if not filesize and duration and fmt.get('tbr'):
                filesize = int(fmt['tbr'] * 1000 / 8 * duration)

            curated.append({
                "format_id": f"res_{h}",
                "quality": label,
                "ext": "mp4",
                "resolution": f"{fmt.get('width', '')}x{h}" if fmt.get('width') else f"{h}p",
                "filesize_approx": filesize,
                "filesize_str": format_filesize(filesize) if filesize else None,
                "has_video": True,
                "has_audio": True,
                "is_recommended": False,
                "vcodec": fmt.get('vcodec'),
                "acodec": fmt.get('acodec')
            })

        if has_any_audio or len(raw_formats) > 0:
            audio_filesize = None
            if best_audio_format:
                audio_filesize = best_audio_format.get('filesize') or best_audio_format.get('filesize_approx')
                if not audio_filesize and duration and best_audio_format.get('tbr'):
                    audio_filesize = int(best_audio_format['tbr'] * 1000 / 8 * duration)

            curated.append({
                "format_id": "audio_mp3",
                "quality": "Audio Only (MP3)",
                "ext": "mp3",
                "resolution": None,
                "filesize_approx": audio_filesize,
                "filesize_str": format_filesize(audio_filesize) if audio_filesize else None,
                "has_video": False,
                "has_audio": True,
                "is_recommended": False,
            })

        return curated


import shutil

class DownloadService:
    """
    Handles downloading and preparing lawful video streams for streaming response.
    """

    @classmethod
    def download_video(cls, url: str, format_id: str = "best") -> Tuple[Path, str, str, int]:
        """
        Downloads the permitted video/audio stream into an isolated temporary folder.
        Returns: (file_path, filename, content_type, file_size)
        """
        task_id = str(uuid.uuid4())
        task_dir = settings.TEMP_DOWNLOAD_DIR / task_id
        task_dir.mkdir(parents=True, exist_ok=True)

        outtmpl = str(task_dir / "%(title).100s.%(ext)s")
        ffmpeg_bin = shutil.which('ffmpeg')

        ydl_opts: Dict[str, Any] = {
            'outtmpl': outtmpl,
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'socket_timeout': settings.DOWNLOAD_TIMEOUT,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            }
        }

        if ffmpeg_bin:
            ydl_opts['ffmpeg_location'] = ffmpeg_bin

        if format_id == "audio_mp3":
            if ffmpeg_bin:
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                ydl_opts.update({
                    'format': 'bestaudio/best',
                })
        elif format_id.startswith("res_"):
            height_str = format_id.replace("res_", "")
            try:
                height = int(height_str)
                ydl_opts.update({
                    'format': f'bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={height}]+bestaudio/best[height<={height}]/best',
                    'merge_output_format': 'mp4',
                })
            except ValueError:
                ydl_opts.update({
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
                    'merge_output_format': 'mp4',
                })
        else:  # "best"
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
            })

        try:
            logger.info(f"Downloading stream for {url} with format {format_id}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if not info:
                    raise ValueError("NO_STREAM: Failed to retrieve downloadable stream.")

                downloaded_files = [f for f in task_dir.glob("*.*") if not f.name.endswith('.part')]
                if not downloaded_files:
                    raise ValueError("DOWNLOAD_EMPTY: Download finished but output file was not found.")

                file_path = downloaded_files[0]
                filename = sanitize_filename(file_path.name)
                file_size = file_path.stat().st_size

                ext = file_path.suffix.lower()
                media_types = {
                    '.mp4': 'video/mp4',
                    '.webm': 'video/webm',
                    '.mkv': 'video/x-matroska',
                    '.mp3': 'audio/mpeg',
                    '.m4a': 'audio/mp4',
                }
                content_type = media_types.get(ext, 'application/octet-stream')

                return file_path, filename, content_type, file_size

        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e).lower()
            logger.warning(f"yt-dlp DownloadError during download for {url}: {error_msg}")
            if task_dir.exists():
                shutil.rmtree(task_dir, ignore_errors=True)

            if "private video" in error_msg or "is private" in error_msg:
                raise ValueError("PRIVATE_VIDEO: This video is private and cannot be downloaded.")
            elif "drm" in error_msg or "protected" in error_msg:
                raise ValueError("DRM_PROTECTED: This video is DRM-protected and cannot be downloaded.")
            elif "sign in" in error_msg or "login" in error_msg or "members-only" in error_msg:
                raise ValueError("RESTRICTED_CONTENT: This video requires authentication or membership.")
            elif "not available" in error_msg or "not found" in error_msg or "404" in error_msg:
                raise ValueError("VIDEO_NOT_FOUND: The requested video is unavailable or has been removed.")
            elif "geo" in error_msg or "country" in error_msg or "blocked" in error_msg:
                raise ValueError("GEO_RESTRICTED: This video is restricted in the server region.")
            else:
                raise ValueError("DOWNLOAD_FAILED: Unable to download the requested media stream.")

        except Exception as e:
            logger.error(f"Download processing failed for {url}: {e}", exc_info=True)
            if task_dir.exists():
                shutil.rmtree(task_dir, ignore_errors=True)
            raise e
