export interface VideoFormat {
  format_id: string;
  quality: string;
  ext: string;
  resolution?: string | null;
  filesize_approx?: number | null;
  filesize_str?: string | null;
  has_video: boolean;
  has_audio: boolean;
  is_recommended?: boolean;
  vcodec?: string | null;
  acodec?: string | null;
}

export interface VideoInfo {
  id: string;
  url: string;
  title: string;
  thumbnail?: string | null;
  duration?: number | null;
  duration_str?: string | null;
  uploader?: string | null;
  uploader_url?: string | null;
  view_count?: number | null;
  description?: string | null;
  formats: VideoFormat[];
}

export interface DownloadStatus {
  task_id: string;
  status: 'preparing' | 'downloading' | 'merging' | 'ready' | 'failed' | 'cancelled';
  progress: number;
  speed_str?: string | null;
  eta_str?: string | null;
  filename?: string | null;
  filesize?: number | null;
  filesize_str?: string | null;
  download_url?: string | null;
  error_message?: string | null;
}

export interface ApiError {
  code: string;
  message: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: ApiError;
}

export type ProcessingState = 
  | 'idle'
  | 'fetching_info'
  | 'preview'
  | 'preparing'
  | 'downloading'
  | 'ready'
  | 'error';
