'use client';

import React from 'react';

export function Hero() {
  return (
    <section className="text-center pt-16 pb-8 md:pt-24 md:pb-12 max-w-3xl mx-auto px-6">
      {/* Main Headline */}
      <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold tracking-tight text-[var(--text-primary)] leading-[1.1] mb-5">
        Download videos. <br className="hidden sm:inline" />
        <span className="text-[var(--text-secondary)] font-normal">YouTube, Instagram & Full Movies.</span>
      </h1>

      {/* Subtitle */}
      <p className="text-base sm:text-lg text-[var(--text-secondary)] font-normal max-w-xl mx-auto leading-relaxed">
        Paste any YouTube video, full movie, or Instagram link to download in high quality MP4 or MP3 audio.
      </p>
    </section>
  );
}
