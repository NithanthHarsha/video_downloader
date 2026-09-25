'use client';

import { useEffect } from 'react';

export function useTheme() {
  useEffect(() => {
    // Remove any legacy dark class from html element
    document.documentElement.classList.remove('dark');
    try {
      localStorage.removeItem('velora_theme');
    } catch {
      // Ignore localStorage errors
    }
  }, []);

  return { theme: 'light', toggleTheme: () => {}, mounted: true };
}
