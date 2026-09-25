'use client';

import React from 'react';
import { Award, Zap, ShieldCheck, Smartphone } from 'lucide-react';

export function FeatureSection() {
  const features = [
    {
      title: 'High Quality',
      description: 'Download available quality up to 4K UHD with genuine audio-video muxing.',
      icon: <Award className="w-5 h-5 text-blue-500" />,
    },
    {
      title: 'Simple',
      description: 'One link. One clean interface. No intrusive ads or confusing redirects.',
      icon: <Zap className="w-5 h-5 text-amber-500" />,
    },
    {
      title: 'Private',
      description: 'No account required. Files are temporary and automatically purged post-download.',
      icon: <ShieldCheck className="w-5 h-5 text-emerald-500" />,
    },
    {
      title: 'Universal',
      description: 'Standard browser downloads compatible with iOS Safari, Android, Mac & Windows.',
      icon: <Smartphone className="w-5 h-5 text-purple-500" />,
    },
  ];

  return (
    <section id="features" className="py-16 md:py-24 border-t border-[var(--border-color)] bg-black/[0.015]">
      <div className="max-w-5xl mx-auto px-6">
        <div className="text-center mb-12 sm:mb-16">
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-[var(--text-primary)]">
            Crafted for clarity
          </h2>
          <p className="text-sm sm:text-base text-[var(--text-secondary)] mt-2">
            Engineered with modern standards and thoughtful restraint.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((item, idx) => (
            <div
              key={idx}
              className="p-6 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-color)] space-y-3.5 shadow-2xs hover:border-[var(--border-hover)] transition-all"
            >
              <div className="w-10 h-10 rounded-xl bg-black/[0.03] flex items-center justify-center">
                {item.icon}
              </div>
              <h3 className="text-base font-bold text-[var(--text-primary)]">
                {item.title}
              </h3>
              <p className="text-xs sm:text-sm text-[var(--text-secondary)] leading-relaxed">
                {item.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
