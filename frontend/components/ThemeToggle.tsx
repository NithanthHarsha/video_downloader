'use client';

import React from 'react';
import { Sun, Moon } from 'lucide-react';
import { useTheme } from '../hooks/useTheme';

export function ThemeToggle() {
  const { theme, toggleTheme, mounted } = useTheme();

  if (!mounted) {
    return (
      <div className="w-9 h-9 rounded-full bg-black/5 dark:bg-white/5 border border-[var(--border-color)]" />
    );
  }

  return (
    <button
      onClick={toggleTheme}
      aria-label="Toggle theme mode"
      className="relative flex items-center justify-center w-9 h-9 rounded-full bg-black/5 dark:bg-white/10 hover:bg-black/10 dark:hover:bg-white/15 border border-[var(--border-color)] transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--accent)]"
    >
      {theme === 'dark' ? (
        <Sun className="w-4 h-4 text-amber-400 transition-transform duration-300 rotate-0 hover:rotate-45" />
      ) : (
        <Moon className="w-4 h-4 text-[var(--text-secondary)] transition-transform duration-300 -rotate-12 hover:rotate-0" />
      )}
    </button>
  );
}
