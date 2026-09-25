'use client';

import React from 'react';
import { Download, Loader2 } from 'lucide-react';
import { ProcessingState } from '../lib/types';

interface DownloadButtonProps {
  state: ProcessingState;
  onClick: () => void;
  disabled?: boolean;
}

export function DownloadButton({ state, onClick, disabled = false }: DownloadButtonProps) {
  const isBusy = state === 'preparing' || state === 'downloading';

  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled || isBusy}
      className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-8 py-3.5 rounded-xl bg-[var(--text-primary)] text-[var(--bg-surface)] dark:bg-[var(--text-primary)] dark:text-[var(--bg-primary)] font-medium text-sm hover:opacity-90 active:scale-[0.98] disabled:opacity-40 disabled:pointer-events-none transition-all shadow-sm"
    >
      {isBusy ? (
        <>
          <Loader2 className="w-4 h-4 animate-spin" />
          <span>Processing Download...</span>
        </>
      ) : (
        <>
          <Download className="w-4 h-4" />
          <span>Download Video</span>
        </>
      )}
    </button>
  );
}
