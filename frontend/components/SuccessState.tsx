'use client';

import React from 'react';
import { CheckCircle, Download, RotateCcw, Smartphone, Laptop } from 'lucide-react';
import { DownloadStatus } from '../lib/types';

interface SuccessStateProps {
  status: DownloadStatus;
  onReset: () => void;
}

export function SuccessState({ status, onReset }: SuccessStateProps) {
  const downloadUrl = status.download_url || '#';
  const filename = status.filename || 'download.mp4';

  return (
    <div className="w-full p-6 sm:p-8 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-color)] shadow-[var(--card-shadow)] text-center space-y-6 animate-in fade-in zoom-in-95 duration-300">
      {/* Icon */}
      <div className="w-16 h-16 rounded-full bg-emerald-500/10 text-[var(--success)] flex items-center justify-center mx-auto ring-8 ring-emerald-500/5">
        <CheckCircle className="w-8 h-8 stroke-[2.5]" />
      </div>

      {/* Heading */}
      <div className="space-y-1.5">
        <h3 className="text-xl sm:text-2xl font-bold tracking-tight text-[var(--text-primary)]">
          Download Ready
        </h3>
        <p className="text-sm text-[var(--text-secondary)] max-w-md mx-auto truncate font-mono bg-black/[0.03] py-1 px-3 rounded-lg border border-[var(--border-color)]">
          {filename} {status.filesize_str ? `(${status.filesize_str})` : ''}
        </p>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
        <a
          href={downloadUrl}
          download={filename}
          className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-6 py-3.5 rounded-xl bg-[var(--accent)] text-white font-medium text-sm hover:opacity-95 active:scale-[0.98] transition-all shadow-md"
        >
          <Download className="w-4 h-4" />
          <span>Save File to Device</span>
        </a>

        <button
          type="button"
          onClick={onReset}
          className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-5 py-3.5 rounded-xl bg-black/5 text-[var(--text-primary)] font-medium text-sm hover:bg-black/10 transition-all border border-[var(--border-color)]"
        >
          <RotateCcw className="w-4 h-4" />
          <span>Download Another</span>
        </button>
      </div>

      {/* Device Guidance Box */}
      <div className="pt-4 border-t border-[var(--border-color)] text-left">
        <div className="p-3.5 rounded-xl bg-black/[0.02] border border-[var(--border-color)] flex items-start space-x-3 text-xs text-[var(--text-secondary)]">
          <Smartphone className="w-4 h-4 shrink-0 text-[var(--text-muted)] mt-0.5" />
          <div>
            <span className="font-semibold text-[var(--text-primary)]">Mobile & Desktop Note: </span>
            Your download is processed directly through your browser. On iPhone (Safari) and Android (Chrome), tap <strong>Save</strong> or <strong>Download</strong> in the browser prompt to store the file in your Files / Downloads.
          </div>
        </div>
      </div>
    </div>
  );
}
