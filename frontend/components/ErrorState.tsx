'use client';

import React from 'react';
import { AlertTriangle, RotateCcw } from 'lucide-react';
import { ApiError } from '../lib/types';

interface ErrorStateProps {
  error: ApiError | null;
  onRetry: () => void;
}

export function ErrorState({ error, onRetry }: ErrorStateProps) {
  if (!error) return null;

  return (
    <div className="w-full p-6 sm:p-8 rounded-2xl bg-[var(--bg-surface)] border border-red-500/20 shadow-[var(--card-shadow)] text-center space-y-4 animate-in fade-in zoom-in-95 duration-200">
      <div className="w-14 h-14 rounded-full bg-red-500/10 text-[var(--error)] flex items-center justify-center mx-auto ring-8 ring-red-500/5">
        <AlertTriangle className="w-7 h-7" />
      </div>

      <div className="space-y-1">
        <h3 className="text-lg font-bold text-[var(--text-primary)]">
          Unable to Process Video
        </h3>
        <p className="text-sm text-[var(--text-secondary)] max-w-md mx-auto">
          {error.message || 'Please check the link and try again.'}
        </p>
      </div>

      <div className="pt-2">
        <button
          type="button"
          onClick={onRetry}
          className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-black/5 text-[var(--text-primary)] font-medium text-sm hover:bg-black/10 transition-all border border-[var(--border-color)]"
        >
          <RotateCcw className="w-4 h-4" />
          <span>Try Another Link</span>
        </button>
      </div>
    </div>
  );
}
