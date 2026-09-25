import React from 'react';
import type { Metadata } from 'next';
import Link from 'next/link';
import { Navbar } from '../../components/Navbar';
import { Footer } from '../../components/Footer';
import {
  Film,
  Music,
  Video,
  Zap,
  ShieldCheck,
  Smartphone,
  CheckCircle,
  Clock,
  Sparkles,
  ArrowRight,
  Download,
  Layers,
} from 'lucide-react';

export const metadata: Metadata = {
  title: 'Features — come on Video Downloader',
  description: 'Explore the high-speed, privacy-first features of come on: 4K video downloads, full movies, Instagram Reels, and MP3 audio extraction.',
};

export default function FeaturesPage() {
  const coreFeatures = [
    {
      icon: <Film className="w-6 h-6 text-purple-600" />,
      title: 'Full Movies & Long Duration Videos',
      badge: 'Up to 10 GB',
      description:
        'Engineered to handle long-form content, documentaries, podcasts, and full movies from YouTube without timeout interruptions or file truncations.',
      details: ['Extended 1-hour processing window', 'Automatic stream reassembly', 'No artificial duration limits'],
    },
    {
      icon: <Video className="w-6 h-6 text-blue-600" />,
      title: 'Crisp 4K UHD & 1080p Full HD',
      badge: 'Ultra HD',
      description:
        'Preserve true original video clarity with hardware-accelerated audio/video merging for pristine MP4 output across all supported resolutions.',
      details: ['Original audio quality preserved', 'Standard MP4 container compatibility', 'Smooth frame-rate retention'],
    },
    {
      icon: <Layers className="w-6 h-6 text-pink-600" />,
      title: 'Instagram Reels, Posts & Clips',
      badge: 'Social Media',
      description:
        'Download high-definition Instagram Reels, video posts, and clips directly by pasting the post link into come on.',
      details: ['Instant progressive MP4 extraction', 'Works with mobile & desktop links', 'No login or app required'],
    },
    {
      icon: <Music className="w-6 h-6 text-amber-600" />,
      title: 'High-Bitrate MP3 Audio Extractor',
      badge: '192 kbps',
      description:
        'Extract crystal clear audio tracks from any video or music session into universal MP3 format for offline listening.',
      details: ['Automatic audio stream isolation', 'Standard ID3 tag compatibility', 'Optimized for music and podcasts'],
    },
    {
      icon: <ShieldCheck className="w-6 h-6 text-emerald-600" />,
      title: 'Privacy-First & Zero Logging',
      badge: '100% Private',
      description:
        'We never track your history, store your downloads, or sell analytics. Media files are wiped immediately upon stream completion.',
      details: ['Automatic post-download cleanup', 'No user account or cookies needed', 'Encrypted HTTPS connections'],
    },
    {
      icon: <Smartphone className="w-6 h-6 text-indigo-600" />,
      title: 'Cross-Device Compatibility',
      badge: 'Universal',
      description:
        'Built with standard HTML5 download streams that work effortlessly on iOS Safari, Android Chrome, Mac, Windows, and Linux.',
      details: ['Direct browser file prompt', 'No desktop executable needed', 'Responsive mobile-first layout'],
    },
  ];

  return (
    <div className="flex flex-col min-h-screen bg-[var(--bg-primary)]">
      <Navbar />

      <main className="flex-1 max-w-5xl mx-auto px-6 py-12 md:py-20 w-full">
        {/* Page Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 md:mb-20">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-black/[0.03] border border-[var(--border-color)] text-xs font-semibold tracking-widest text-[var(--text-secondary)] uppercase mb-5">
            <Sparkles className="w-3.5 h-3.5 text-[var(--accent)]" />
            <span>POWERFUL & STREAMLINED</span>
          </div>

          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-[var(--text-primary)] leading-tight mb-5">
            Engineered for pure speed, <br />
            clarity and simplicity.
          </h1>

          <p className="text-base sm:text-lg text-[var(--text-secondary)] leading-relaxed">
            Everything you need to download public videos, full movies, and Instagram Reels in top quality with zero bloat.
          </p>
        </div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8 mb-20">
          {coreFeatures.map((feat, idx) => (
            <div
              key={idx}
              className="p-7 sm:p-8 rounded-2xl bg-[var(--bg-surface)] border border-[var(--border-color)] shadow-[var(--card-shadow)] space-y-4 hover:border-[var(--border-hover)] transition-all duration-200"
            >
              <div className="flex items-center justify-between">
                <div className="p-2.5 rounded-xl bg-black/[0.03]">
                  {feat.icon}
                </div>
                <span className="px-2.5 py-1 rounded-md text-xs font-medium bg-black/[0.04] text-[var(--text-secondary)] border border-[var(--border-color)]">
                  {feat.badge}
                </span>
              </div>

              <h2 className="text-xl font-bold text-[var(--text-primary)]">
                {feat.title}
              </h2>

              <p className="text-sm text-[var(--text-secondary)] leading-relaxed">
                {feat.description}
              </p>

              <div className="pt-2 border-t border-[var(--border-color)] space-y-1.5">
                {feat.details.map((d, dIdx) => (
                  <div key={dIdx} className="flex items-center space-x-2 text-xs text-[var(--text-secondary)]">
                    <CheckCircle className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                    <span>{d}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* CTA Card */}
        <div className="p-8 sm:p-12 rounded-3xl bg-[var(--bg-surface)] border border-[var(--border-color)] shadow-[var(--card-shadow)] text-center space-y-6">
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-[var(--text-primary)]">
            Ready to download your first video?
          </h2>
          <p className="text-sm sm:text-base text-[var(--text-secondary)] max-w-xl mx-auto">
            Paste any public YouTube video, full movie, or Instagram Reel link and experience seamless high-speed downloads.
          </p>
          <div className="pt-2">
            <Link
              href="/"
              className="inline-flex items-center space-x-2 px-7 py-3.5 rounded-xl bg-[var(--text-primary)] text-[var(--bg-surface)] font-medium text-sm hover:opacity-90 active:scale-[0.98] transition-all shadow-md"
            >
              <span>Go to Downloader</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
