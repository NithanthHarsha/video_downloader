'use client';

import React, { useState } from 'react';
import { VideoInfo, ProcessingState, DownloadStatus } from '../lib/types';
import { QualitySelector } from './QualitySelector';
import { DownloadButton } from './DownloadButton';
import { DownloadProgress } from './DownloadProgress';
import { Clock, User, Eye, ArrowLeft, Film } from 'lucide-react';

interface VideoPreviewProps {
  video: VideoInfo;
  state: ProcessingState;
  downloadStatus: DownloadStatus | null;
  onStartDownload: (formatId: string) => void;
  onReset: () => void;
}

export function VideoPreview({
  video,
  state,
  downloadStatus,
  onStartDownload,
  onReset,
}: VideoPreviewProps) {
  // Find recommended format or fallback to first
  const initialFormat =
    video.formats.find((f) => f.is_recommended)?.format_id ||
    video.formats[0]?.format_id ||
    'best';

  const [selectedFormatId, setSelectedFormatId] = useState<string>(initialFormat);

  const isBusy = state === 'preparing' || state === 'downloading';

  return (
    <div className="w-full max-w-2xl mx-auto bg-[var(--bg-surface)] rounded-2xl border border-[var(--border-color)] p-5 sm:p-7 shadow-[var(--card-shadow)] space-y-6 animate-in fade-in slide-in-from-bottom-3 duration-300">
      {/* Top Bar: Back / Change URL */}
      <div className="flex items-center justify-between pb-4 border-b border-[var(--border-color)]">
        <button
          type="button"
          onClick={onReset}
          disabled={isBusy}
          className="inline-flex items-center space-x-1.5 text-xs font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] disabled:opacity-50 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Change URL</span>
        </button>

        <span className="text-xs text-[var(--text-muted)] font-mono">
          Ready to save
        </span>
      </div>

      {/* Main Video Info Box */}
      <div className="flex flex-col sm:flex-row gap-5 items-start">
        {/* Thumbnail Preview */}
        <div className="relative w-full sm:w-48 aspect-video rounded-xl overflow-hidden bg-black/5 border border-[var(--border-color)] shrink-0 group">
          {video.thumbnail ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={video.thumbnail}
              alt={video.title}
              className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-[var(--text-muted)]">
              <Film className="w-8 h-8 opacity-40" />
            </div>
          )}

          {/* Duration Badge */}
          {video.duration_str && (
            <div className="absolute bottom-2 right-2 px-1.5 py-0.5 rounded-md bg-black/80 backdrop-blur-xs text-[11px] font-mono font-medium text-white flex items-center space-x-1">
              <Clock className="w-2.5 h-2.5" />
              <span>{video.duration_str}</span>
            </div>
          )}
        </div>

        {/* Video Title and Metadata */}
        <div className="flex-1 min-w-0 space-y-2">
          <h2 className="text-base sm:text-lg font-semibold tracking-tight text-[var(--text-primary)] line-clamp-2 leading-snug">
            {video.title}
          </h2>

          <div className="flex flex-wrap items-center gap-y-1 gap-x-3 text-xs text-[var(--text-secondary)]">
            {video.uploader && (
              <div className="flex items-center space-x-1">
                <User className="w-3.5 h-3.5 text-[var(--text-muted)]" />
                <span className="font-medium truncate max-w-[160px]">{video.uploader}</span>
              </div>
            )}

            {video.view_count && (
              <div className="flex items-center space-x-1 text-[var(--text-muted)]">
                <Eye className="w-3.5 h-3.5" />
                <span>{video.view_count.toLocaleString()} views</span>
              </div>
            )}
          </div>

          {video.description && (
            <p className="text-xs text-[var(--text-muted)] line-clamp-2 pt-1">
              {video.description}
            </p>
          )}
        </div>
      </div>

      {/* Quality / Resolution Selection */}
      <QualitySelector
        formats={video.formats}
        selectedFormatId={selectedFormatId}
        onSelectFormat={setSelectedFormatId}
        disabled={isBusy}
      />

      {/* Real-time Progress Bar when actively downloading */}
      {isBusy && <DownloadProgress status={downloadStatus} />}

      {/* Action CTA */}
      <div className="flex items-center justify-end pt-2">
        <DownloadButton
          state={state}
          onClick={() => onStartDownload(selectedFormatId)}
          disabled={!selectedFormatId}
        />
      </div>
    </div>
  );
}
