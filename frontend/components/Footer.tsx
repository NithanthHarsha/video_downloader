'use client';

import React from 'react';
import Link from 'next/link';

export function Footer() {
  return (
    <footer id="privacy" className="border-t border-[var(--border-color)] bg-[var(--bg-surface)] py-12 px-6 mt-auto">
      <div className="max-w-5xl mx-auto space-y-8">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-2">
            <Link href="/" className="inline-block">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src="/logo.png"
                alt="Come on Logo"
                className="h-12 sm:h-14 w-auto object-contain"
              />
            </Link>
            <p className="text-xs sm:text-sm text-[var(--text-secondary)] max-w-sm">
              Simple video downloading for content you have permission to save.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-6 text-xs text-[var(--text-secondary)]">
            <Link href="/#how-it-works" className="hover:text-[var(--text-primary)] transition-colors">
              How it works
            </Link>
            <Link href="/features" className="hover:text-[var(--text-primary)] transition-colors">
              Features
            </Link>
            <Link href="/privacy" className="hover:text-[var(--text-primary)] transition-colors">
              Privacy Policy
            </Link>
          </div>
        </div>

        <div id="legal-notice" className="pt-6 border-t border-[var(--border-color)] space-y-3">
          <p className="text-[11px] text-[var(--text-muted)] leading-relaxed">
            <strong>Legal Notice:</strong> come on is designed exclusively for public media that you own, have explicit legal rights to, or is in the public domain. come on strictly refuses and does not provide mechanisms to bypass DRM, copy protections, or private access controls.
          </p>

          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between text-[11px] text-[var(--text-muted)] gap-2">
            <span>© 2026 come on. All rights reserved.</span>
            <span>Temporary processing • Zero permanent storage</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
