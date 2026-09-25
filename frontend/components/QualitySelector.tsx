'use client';

import React from 'react';
import { VideoFormat } from '../lib/types';
import { Check, Video, Music, Sparkles } from 'lucide-react';

interface QualitySelectorProps {
  formats: VideoFormat[];
  selectedFormatId: string;
  onSelectFormat: (formatId: string) => void;
  disabled?: boolean;
}

export function QualitySelector({
  formats,
  selectedFormatId,
  onSelectFormat,
  disabled = false,
}: QualitySelectorProps) {
  if (!formats || formats.length === 0) {
    return null;
  }

  return (
    <div className="w-full space-y-2.5">
      <label className="text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)]">
        Select Quality / Format
      </label>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        {formats.map((fmt) => {
          const isSelected = fmt.format_id === selectedFormatId;
          const isAudioOnly = !fmt.has_video && fmt.has_audio;

          return (
            <button
              key={fmt.format_id}
              type="button"
              disabled={disabled}
              onClick={() => onSelectFormat(fmt.format_id)}
              className={`relative flex items-center justify-between p-3.5 rounded-xl border text-left transition-all duration-200 ${
                isSelected
                  ? 'bg-black/[0.04] border-[var(--text-primary)] ring-1 ring-[var(--text-primary)]'
                  : 'bg-[var(--bg-surface)] border-[var(--border-color)] hover:border-[var(--border-hover)]'
              } disabled:opacity-50 disabled:pointer-events-none`}
            >
              <div className="flex items-center space-x-3 min-w-0">
                <div
                  className={`p-2 rounded-lg ${
                    isAudioOnly
                      ? 'bg-amber-500/10 text-amber-600'
                      : 'bg-blue-500/10 text-blue-600'
                  }`}
                >
                  {isAudioOnly ? (
                    <Music className="w-4 h-4" />
                  ) : (
                    <Video className="w-4 h-4" />
                  )}
                </div>

                <div className="min-w-0">
                  <div className="flex items-center space-x-1.5">
                    <span className="text-sm font-medium text-[var(--text-primary)] truncate">
                      {fmt.quality}
                    </span>
                    {fmt.is_recommended && (
                      <span className="inline-flex items-center px-1.5 py-0.5 rounded-md text-[10px] font-semibold bg-emerald-500/10 text-emerald-600 border border-emerald-500/20">
                        <Sparkles className="w-2.5 h-2.5 mr-0.5" />
                        Best
                      </span>
                    )}
                  </div>
                  <div className="text-xs text-[var(--text-muted)] flex items-center space-x-2 mt-0.5">
                    <span className="uppercase">{fmt.ext}</span>
                    {fmt.filesize_str && (
                      <>
                        <span>•</span>
                        <span>{fmt.filesize_str}</span>
                      </>
                    )}
                  </div>
                </div>
              </div>

              {isSelected && (
                <div className="w-5 h-5 rounded-full bg-[var(--text-primary)] text-[var(--bg-surface)] flex items-center justify-center shrink-0 ml-2">
                  <Check className="w-3 h-3 stroke-[3]" />
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
