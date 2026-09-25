'use client';

import React from 'react';
import { Link2, Sliders, ArrowDownToLine } from 'lucide-react';

export function HowItWorks() {
  const steps = [
    {
      number: '01',
      title: 'Paste',
      description: 'Paste your public video link into the input box.',
      icon: <Link2 className="w-5 h-5 text-[var(--accent)]" />,
    },
    {
      number: '02',
      title: 'Choose',
      description: 'Select the quality available for your permitted download.',
      icon: <Sliders className="w-5 h-5 text-purple-600" />,
    },
    {
      number: '03',
      title: 'Download',
      description: 'Save the file smoothly through your browser.',
      icon: <ArrowDownToLine className="w-5 h-5 text-emerald-600" />,
    },
  ];

  return (
    <section id="how-it-works" className="py-16 md:py-24 max-w-5xl mx-auto px-6">
      <div className="text-center mb-12 sm:mb-16">
        <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-[var(--text-primary)]">
          How it works
        </h2>
        <p className="text-sm sm:text-base text-[var(--text-secondary)] mt-2">
          Three simple steps to save public media on any device.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
        {steps.map((step) => (
          <div
            key={step.number}
            className="p-6 sm:p-7 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-color)] shadow-xs space-y-4 hover:border-[var(--border-hover)] transition-all duration-200"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono font-bold tracking-wider text-[var(--text-muted)]">
                {step.number}
              </span>
              <div className="p-2 rounded-xl bg-black/[0.03]">
                {step.icon}
              </div>
            </div>

            <div className="space-y-1.5">
              <h3 className="text-lg font-bold text-[var(--text-primary)]">
                {step.title}
              </h3>
              <p className="text-sm text-[var(--text-secondary)] leading-relaxed">
                {step.description}
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
