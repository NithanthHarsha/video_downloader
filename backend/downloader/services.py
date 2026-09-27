import os
import uuid
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import importlib.metadata
import json
import subprocess
import shutil
import time
import urllib.request
import yt_dlp
from django.conf import settings
from .utils import sanitize_filename, format_duration, format_filesize

logger = logging.getLogger(__name__)

_pot_server_process = None


def check_pot_server_health(host: str = "127.0.0.1", port: int = 4416) -> bool:
    """
    Checks if the local bgutil PO token server is responding on the given port.
    """
    try:
        req = urllib.request.Request(
            f"http://{host}:{port}/ping",
            headers={"User-Agent": "yt-dlp-pot-checker"}
        )
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode())
                version = data.get("version", "")
                return bool(version.startswith("2.") or data.get("status") == "ok")
    except Exception:
        pass
    return False


def ensure_pot_server_running() -> bool:
    """
    Ensures the local bgutil PO Token Provider HTTP server (v2.0.0) is running on 127.0.0.1:4416
    if built and available, without blocking on compilation.
    """
    global _pot_server_process
    if check_pot_server_health():
        return True

    bgutil_candidates = [
        settings.BASE_DIR / "bgutil-server",
        Path.cwd() / "bgutil-server",
        Path.home() / "bgutil-server",
        Path("/opt/render/project/src/backend/bgutil-server"),
    ]

    bgutil_dir = None
    for cand in bgutil_candidates:
        if cand.exists() and (cand / "package.json").exists():
            bgutil_dir = cand
            break

    if not bgutil_dir:
        return False

    main_js = bgutil_dir / "build" / "main.js"
    node_bin = shutil.which('node') or 'node'

    if main_js.exists() and _pot_server_process is None:
        try:
            logger.info(f"Starting bgutil PO Token server in '{bgutil_dir}' on 127.0.0.1:4416...")
            _pot_server_process = subprocess.Popen(
                [node_bin, str(main_js), "--port", "4416", "--host", "127.0.0.1"],
                cwd=str(bgutil_dir),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            for _ in range(5):
                time.sleep(0.1)
                if check_pot_server_health():
                    logger.info("[POT Supervisor] bgutil PO token server is healthy and active on 127.0.0.1:4416")
                    return True
        except Exception as err:
            logger.warning(f"Failed to spawn bgutil server process: {err}")

    return check_pot_server_health()


def _get_binary_version(binary_path: str) -> Optional[str]:
    try:
        res = subprocess.run([binary_path, "--version"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0 and res.stdout:
            return res.stdout.strip().splitlines()[0]
    except Exception:
        pass
    return None


def get_discovered_js_runtimes() -> Dict[str, Dict[str, Any]]:
    """
    Discovers available JavaScript runtimes (Deno, Node, QuickJS, Bun)
    to power yt-dlp YouTube EJS challenge solvers. Deno is the primary
    runtime recommended by yt-dlp.
    """
    runtimes: Dict[str, Dict[str, Any]] = {}

    # 1. Check for Deno (primary recommendation for yt-dlp EJS)
    deno_bin = shutil.which('deno')
    if not deno_bin:
        deno_candidates = [
            Path.home() / ".deno" / "bin" / ("deno.exe" if os.name == "nt" else "deno"),
            Path("/opt/render/.deno/bin/deno"),
            Path("/root/.deno/bin/deno"),
            Path("/usr/local/bin/deno"),
            Path("/usr/bin/deno"),
        ]
        for candidate in deno_candidates:
            if candidate.exists() and os.access(candidate, os.X_OK if hasattr(os, 'X_OK') else os.F_OK):
                deno_bin = str(candidate)
                break

    if deno_bin:
        runtimes['deno'] = {'path': str(deno_bin)}
        deno_version = _get_binary_version(str(deno_bin))
        logger.info(f"[Diagnostics] Detected Deno runtime at '{deno_bin}' (Version: {deno_version or 'unknown'})")
    else:
        runtimes['deno'] = {}

    # 2. Check for Node.js (supported fallback)
    node_bin = shutil.which('node')
    if not node_bin:
        node_candidates = [
            Path("/usr/local/bin/node"),
            Path("/usr/bin/node"),
            Path("/opt/render/project/src/.nodejs/bin/node"),
        ]
        for candidate in node_candidates:
            if candidate.exists() and os.access(candidate, os.X_OK if hasattr(os, 'X_OK') else os.F_OK):
                node_bin = str(candidate)
                break

    if node_bin:
        runtimes['node'] = {'path': str(node_bin)}
        node_version = _get_binary_version(str(node_bin))
        logger.info(f"[Diagnostics] Detected Node runtime at '{node_bin}' (Version: {node_version or 'unknown'})")
    else:
        runtimes['node'] = {}

    # 3. QuickJS and Bun fallbacks
    quickjs_bin = shutil.which('quickjs') or shutil.which('qjs')
    if quickjs_bin:
        runtimes['quickjs'] = {'path': str(quickjs_bin)}

    bun_bin = shutil.which('bun')
    if bun_bin:
        runtimes['bun'] = {'path': str(bun_bin)}

    return runtimes


def log_extraction_diagnostics(url: str):
    """
    Logs safe runtime diagnostics for yt-dlp execution without exposing credentials or tokens.
    """
    try:
        ytdlp_ver = getattr(yt_dlp.version, '__version__', 'unknown')
    except Exception:
        ytdlp_ver = 'unknown'

    try:
        ejs_ver = importlib.metadata.version('yt-dlp-ejs')
    except Exception:
        ejs_ver = 'not-installed'

    try:
        pot_pkg_ver = importlib.metadata.version('bgutil-ytdlp-pot-provider')
    except Exception:
        pot_pkg_ver = 'not-installed'

    provider_registered = False
    try:
        from yt_dlp.extractor.youtube.pot._registry import _pot_providers
        provider_registered = any('BgUtil' in k or 'bgutil' in str(v).lower() for k, v in _pot_providers.items())
    except Exception:
        pass

    bgutil_reachable = check_pot_server_health()
    runtimes = get_discovered_js_runtimes()
    deno_ver = _get_binary_version(runtimes.get('deno', {}).get('path', '')) if runtimes.get('deno', {}).get('path') else 'not-found'
    node_ver = _get_binary_version(runtimes.get('node', {}).get('path', '')) if runtimes.get('node', {}).get('path') else 'not-found'

    logger.info(
        f"[YT DIAGNOSTICS] yt_dlp_version={ytdlp_ver} | "
        f"yt_dlp_ejs_version={ejs_ver} | "
        f"bgutil_provider_version={pot_pkg_ver} | "
        f"provider_registered={provider_registered} | "
        f"bgutil_reachable={bgutil_reachable} | "
        f"deno_version={deno_ver} | "
        f"node_version={node_ver} | "
        f"target_url={url}"
    )


def get_base_ydl_opts() -> Dict[str, Any]:
    """
    Returns standard yt-dlp configuration with JS runtimes and PO token provider enabled
    for solving YouTube EJS JavaScript challenges and Proof of Origin tokens safely.
    """
    ensure_pot_server_running()

    bgutil_server_path = str(settings.BASE_DIR / 'bgutil-server')

    opts: Dict[str, Any] = {
        'quiet': True,
        'no_warnings': False,
        'noplaylist': True,
        'js_runtimes': get_discovered_js_runtimes(),
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android', 'mweb', 'web'],
            },
            'youtubepot-bgutilhttp': {
                'base_url': ['http://127.0.0.1:4416'],
            },
            'youtubepot-bgutilscript': {
                'server_home': [bgutil_server_path],
            },
        },
    }

    return opts


def _classify_ytdlp_error(raw_err: str, is_download: bool = False) -> Tuple[str, str]:
    """
    Parses yt-dlp DownloadError string and classifies it into standard error code and user-facing message.
    Distinguishes strictly between actual access restrictions (private, members-only, age-restricted)
    and technical extraction failures.
    """
    error_lower = raw_err.lower()

    # Private video
    if "private video" in error_lower or "is private" in error_lower or "this video is private" in error_lower:
        return "PRIVATE_VIDEO", "This video is private and requires authorized access."

    # Members-only video
    if "members-only" in error_lower or "members only" in error_lower or "join this channel" in error_lower or "channel member" in error_lower:
        return "MEMBERS_ONLY", "This video is members-only and requires a channel membership."

    # Age-restricted video
    if "confirm your age" in error_lower or "age-restricted" in error_lower or "inappropriate for some users" in error_lower:
        return "AGE_RESTRICTED", "This video is age-restricted and requires account verification."

    # Account authentication / login required (specifically for viewing restricted content, not bot detection)
    if ("sign in to view" in error_lower or "login required" in error_lower or "account required" in error_lower) and "bot" not in error_lower:
        return "AUTH_REQUIRED", "This video requires authorized account access."

    # DRM Protected
    if "drm" in error_lower or "protected" in error_lower:
        action = "downloaded" if is_download else "accessed"
        return "DRM_PROTECTED", f"This video is DRM-protected and cannot be {action}."

    # Geographic restrictions
    if "not available in your country" in error_lower or "geo" in error_lower or "country" in error_lower or "blocked in your country" in error_lower or "uploader has not made this video available in your country" in error_lower:
        return "GEO_RESTRICTED", "This video is restricted in the server region."

    # Video not found or deleted
    if "not available" in error_lower or "unavailable" in error_lower or "not found" in error_lower or "404" in error_lower or "removed by" in error_lower or "does not exist" in error_lower:
        return "VIDEO_NOT_FOUND", "The requested video could not be found or is unavailable."

    # Unsupported URL
    if "unsupported url" in error_lower:
        return "UNSUPPORTED_URL", "The provided URL is not supported."

    # Technical extraction or download error
    prefix = "DOWNLOAD_FAILED" if is_download else "EXTRACTION_FAILED"
    cleaned_msg = raw_err.replace("ERROR: ", "").replace("WARNING: ", "").strip()
    lines = [line.strip() for line in cleaned_msg.splitlines() if line.strip()]
    final_msg = lines[0] if lines else "Extraction failed. Please verify the URL."
    return prefix, final_msg


class VideoService:
    """
    Handles extracting video metadata and determining available formats
    using yt-dlp in a safe, lawful manner.
    """

    @staticmethod
    def get_ydl_opts() -> Dict[str, Any]:
        opts = get_base_ydl_opts()
        opts.update({
            'skip_download': True,
            'extract_flat': False,
            'socket_timeout': 30,
        })
        return opts

    @classmethod
    def extract_info(cls, url: str) -> Dict[str, Any]:
        """
        Extracts video metadata from a public URL.
        """
        log_extraction_diagnostics(url)
        ydl_opts = cls.get_ydl_opts()

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    raise ValueError("NO_DATA: No metadata returned for this video.")

                if 'entries' in info and info['entries']:
                    info = info['entries'][0]

                extractor_used = info.get('extractor') or info.get('extractor_key') or 'unknown'
                logger.info(f"[Diagnostics] Extraction successful for {url} using extractor: {extractor_used}")
                return cls._parse_video_info(url, info)

        except yt_dlp.utils.DownloadError as e:
            raw_err = str(e)
            code, user_msg = _classify_ytdlp_error(raw_err, is_download=False)
            logger.error(f"[yt-dlp DownloadError] URL: {url} | Code: {code} | Details: {raw_err}", exc_info=True)
            raise ValueError(f"{code}: {user_msg}")

        except Exception as e:
            logger.error(f"[Unexpected Extraction Error] URL: {url} | Type: {type(e).__name__} | Details: {e}", exc_info=True)
            if ":" in str(e) and str(e).split(":")[0].isupper():
                raise e
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

        ydl_opts = get_base_ydl_opts()
        ydl_opts.update({
            'outtmpl': outtmpl,
            'socket_timeout': settings.DOWNLOAD_TIMEOUT,
        })

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
            raw_err = str(e)
            if task_dir.exists():
                shutil.rmtree(task_dir, ignore_errors=True)
            code, user_msg = _classify_ytdlp_error(raw_err, is_download=True)
            logger.error(f"[yt-dlp DownloadError during download] URL: {url} | Code: {code} | Details: {raw_err}", exc_info=True)
            raise ValueError(f"{code}: {user_msg}")

        except Exception as e:
            logger.error(f"[Unexpected Download Error] URL: {url} | Type: {type(e).__name__} | Details: {e}", exc_info=True)
            if task_dir.exists():
                shutil.rmtree(task_dir, ignore_errors=True)
            if ":" in str(e) and str(e).split(":")[0].isupper():
                raise e
            raise ValueError(f"DOWNLOAD_FAILED: {str(e)}")
