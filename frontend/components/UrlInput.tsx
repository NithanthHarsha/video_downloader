'use client';

import React, { useState } from 'react';
import { Clipboard, X, ArrowRight, Loader2, Link2, AlertCircle } from 'lucide-react';
import { isValidUrlString } from '../lib/utils';

interface UrlInputProps {
  onAnalyze: (url: string) => void;
  isLoading: boolean;
  disabled?: boolean;
}

export function UrlInput({ onAnalyze, isLoading, disabled = false }: UrlInputProps) {
  const [url, setUrl] = useState('');
  const [validationError, setValidationError] = useState<string | null>(null);

  const handlePaste = async () => {
    try {
      if (navigator.clipboard && navigator.clipboard.readText) {
        const text = await navigator.clipboard.readText();
        if (text) {
          setUrl(text.trim());
          setValidationError(null);
        }
      }
    } catch {
      // Clipboard permissions denied or unavailable
    }
  };

  const handleClear = () => {
    setUrl('');
    setValidationError(null);
  };

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (isLoading || disabled) return;

    const trimmed = url.trim();
    if (!trimmed) {
      setValidationError('Please paste or type a video link.');
      return;
    }

    if (!isValidUrlString(trimmed)) {
      setValidationError('Please enter a valid URL starting with http:// or https://');
      return;
    }

    setValidationError(null);
    onAnalyze(trimmed);
  };

  return (
    <div className="w-full max-w-2xl mx-auto px-4 sm:px-0">
      <form onSubmit={handleSubmit} className="relative">
        <div className="group relative flex items-center bg-[var(--bg-surface)] rounded-2xl border border-[var(--border-color)] p-2 sm:p-2.5 shadow-[var(--input-shadow)] transition-all duration-300 focus-within:border-[var(--accent)] focus-within:ring-4 focus-within:ring-[var(--accent-subtle)]">
          {/* Icon */}
          <div className="pl-3 pr-2 text-[var(--text-muted)] hidden sm:block">
            <Link2 className="w-5 h-5" />
          </div>

          {/* Text input */}
          <input
            type="url"
            value={url}
            onChange={(e) => {
              setUrl(e.target.value);
              if (validationError) setValidationError(null);
            }}
            placeholder="Paste YouTube video, full movie, or Instagram link..."
            disabled={isLoading || disabled}
            aria-label="Video URL input"
            className="flex-1 bg-transparent px-2 py-3 text-base text-[var(--text-primary)] placeholder:text-[var(--text-muted)] focus:outline-none disabled:opacity-50 min-w-0"
          />

          {/* Action buttons (Clear / Paste) */}
          <div className="flex items-center space-x-1.5 px-1">
            {url ? (
              <button
                type="button"
                onClick={handleClear}
                disabled={isLoading || disabled}
                aria-label="Clear URL"
                className="p-1.5 rounded-full text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-black/5 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            ) : (
              <button
                type="button"
                onClick={handlePaste}
                disabled={isLoading || disabled}
                aria-label="Paste from clipboard"
                className="hidden sm:flex items-center space-x-1 px-2.5 py-1.5 rounded-lg text-xs font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-black/5 transition-colors border border-[var(--border-color)]"
              >
                <Clipboard className="w-3.5 h-3.5" />
                <span>Paste</span>
              </button>
            )}

            {/* Submit / Download button */}
            <button
              type="submit"
              disabled={isLoading || disabled || !url.trim()}
              className="inline-flex items-center justify-center space-x-2 px-5 py-3 rounded-xl bg-[var(--text-primary)] text-[var(--bg-surface)] font-medium text-sm hover:opacity-90 active:scale-[0.98] disabled:opacity-30 disabled:pointer-events-none transition-all shadow-xs"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span className="hidden sm:inline">Checking...</span>
                </>
              ) : (
                <>
                  <span>Download</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </div>
      </form>

      {/* Validation Message */}
      {validationError && (
        <div className="mt-3 flex items-center space-x-2 text-xs text-[var(--error)] animate-in fade-in slide-in-from-top-1 px-3">
          <AlertCircle className="w-3.5 h-3.5 shrink-0" />
          <span>{validationError}</span>
        </div>
      )}

      {/* Helper text */}
      <div className="mt-3 text-center">
        <p className="text-xs text-[var(--text-muted)]">
          Supports YouTube videos & full movies, Instagram Reels & posts • 4K / 1080p / MP3 • No account required
        </p>
      </div>
    </div>
  );
}
