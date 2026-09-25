'use client';

import React from 'react';
import { DownloadStatus } from '../lib/types';
import { Loader2, ArrowDownCircle, Cpu, CheckCircle2 } from 'lucide-react';

interface DownloadProgressProps {
  status: DownloadStatus | null;
}

export function DownloadProgress({ status }: DownloadProgressProps) {
  if (!status) return null;

  const getStatusDetails = () => {
    switch (status.status) {
      case 'preparing':
        return {
          title: 'Preparing Stream',
          desc: 'Connecting to host and fetching video manifest...',
          icon: <Loader2 className="w-5 h-5 animate-spin text-[var(--accent)]" />,
          indeterminate: true,
        };
      case 'downloading':
        return {
          title: 'Downloading Video',
          desc: `${status.speed_str ? `Speed: ${status.speed_str}` : 'Transferring data'} ${
            status.eta_str ? `• ETA: ${status.eta_str}` : ''
          }`,
          icon: <ArrowDownCircle className="w-5 h-5 text-[var(--accent)] animate-pulse" />,
          indeterminate: false,
        };
      case 'merging':
        return {
          title: 'Finalizing & Converting',
          desc: 'Processing media codecs and merging audio/video tracks...',
          icon: <Cpu className="w-5 h-5 text-amber-500 animate-pulse" />,
          indeterminate: true,
        };
      case 'ready':
        return {
          title: 'Ready to Save',
          desc: 'Download completed. Initializing browser transfer...',
          icon: <CheckCircle2 className="w-5 h-5 text-[var(--success)]" />,
          indeterminate: false,
        };
      default:
        return {
          title: 'Processing...',
          desc: 'Working on your request...',
          icon: <Loader2 className="w-5 h-5 animate-spin text-[var(--text-secondary)]" />,
          indeterminate: true,
        };
    }
  };

  const { title, desc, icon, indeterminate } = getStatusDetails();

  return (
    <div className="w-full p-4 rounded-xl bg-black/[0.03] border border-[var(--border-color)] space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2.5">
          {icon}
          <div>
            <div className="text-sm font-semibold text-[var(--text-primary)]">{title}</div>
            <div className="text-xs text-[var(--text-secondary)]">{desc}</div>
          </div>
        </div>

        {!indeterminate && (
          <span className="text-sm font-mono font-medium text-[var(--text-primary)]">
            {Math.round(status.progress)}%
          </span>
        )}
      </div>

      {/* Progress Track */}
      <div className="w-full h-2 rounded-full bg-black/10 overflow-hidden relative">
        {indeterminate ? (
          <div className="h-full bg-[var(--accent)] rounded-full w-1/3 animate-[indeterminate_1.5s_infinite_linear]" />
        ) : (
          <div
            className="h-full bg-[var(--accent)] rounded-full transition-all duration-300 ease-out"
            style={{ width: `${Math.min(100, Math.max(0, status.progress))}%` }}
          />
        )}
      </div>
    </div>
  );
}
