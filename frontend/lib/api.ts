import { ApiResponse, VideoInfo, DownloadStatus } from './types';

const API_BASE_URL = (process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000').replace(/\/+$/, '');

export async function fetchVideoInfo(url: string): Promise<ApiResponse<VideoInfo>> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/video/info/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });

    if (!res.ok) {
      if (res.status === 429) {
        return {
          success: false,
          error: {
            code: 'RATE_LIMITED',
            message: 'Too many requests. Please wait a moment and try again.',
          },
        };
      }
      const errData = await res.json().catch(() => null);
      return {
        success: false,
        error: {
          code: errData?.error?.code || 'SERVER_ERROR',
          message: errData?.error?.message || 'Server encountered an issue processing the video URL.',
        },
      };
    }

    const data: ApiResponse<VideoInfo> = await res.json();
    return data;
  } catch (error) {
    return {
      success: false,
      error: {
        code: 'NETWORK_ERROR',
        message: 'Could not connect to the Django API service. Please verify the backend is running.',
      },
    };
  }
}

export async function processAndDownloadVideo(
  url: string,
  formatId: string
): Promise<{ success: boolean; filename?: string; blobUrl?: string; error?: { code: string; message: string } }> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/video/download/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url, format_id: formatId, quality: formatId }),
    });

    if (!res.ok) {
      if (res.status === 429) {
        return {
          success: false,
          error: {
            code: 'RATE_LIMITED',
            message: 'Download rate limit reached. Please wait a moment.',
          },
        };
      }
      const errData = await res.json().catch(() => null);
      return {
        success: false,
        error: {
          code: errData?.error?.code || 'DOWNLOAD_ERROR',
          message: errData?.error?.message || 'Failed to download and prepare video stream.',
        },
      };
    }

    // Extract filename from Content-Disposition header if available
    let filename = formatId === 'audio_mp3' ? 'download.mp3' : 'download.mp4';
    const disposition = res.headers.get('Content-Disposition');
    if (disposition && disposition.includes('filename=')) {
      const match = disposition.match(/filename="?([^"]+)"?/);
      if (match && match[1]) {
        filename = match[1];
      }
    }

    const blob = await res.blob();
    const blobUrl = window.URL.createObjectURL(blob);

    // Trigger native browser download
    const link = document.createElement('a');
    link.href = blobUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    return {
      success: true,
      filename,
      blobUrl,
    };
  } catch (error) {
    return {
      success: false,
      error: {
        code: 'NETWORK_ERROR',
        message: 'Network connection lost during file download.',
      },
    };
  }
}
