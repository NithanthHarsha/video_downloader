import React from 'react';
import type { Metadata } from 'next';
import Link from 'next/link';
import { Navbar } from '../../components/Navbar';
import { Footer } from '../../components/Footer';
import { ShieldCheck, Lock, Trash2, Globe, FileText, ArrowLeft } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Privacy Policy & Terms — come on Video Downloader',
  description: 'Understand how come on respects your privacy: zero permanent storage, instant post-stream file purging, and lawful usage policies.',
};

export default function PrivacyPage() {
  return (
    <div className="flex flex-col min-h-screen bg-[var(--bg-primary)]">
      <Navbar />

      <main className="flex-1 max-w-4xl mx-auto px-6 py-12 md:py-20 w-full">
        {/* Back Link */}
        <div className="mb-8">
          <Link
            href="/"
            className="inline-flex items-center space-x-1.5 text-xs font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Downloader</span>
          </Link>
        </div>

        {/* Page Header */}
        <div className="space-y-3 mb-12 border-b border-[var(--border-color)] pb-8">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-semibold text-emerald-600">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>PRIVACY & LEGAL POLICY</span>
          </div>

          <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-[var(--text-primary)]">
            Privacy Policy & Terms of Service
          </h1>

          <p className="text-sm text-[var(--text-secondary)]">
            Last updated: September 2026 • Effective immediately
          </p>
        </div>

        {/* Content Sections */}
        <div className="space-y-10 text-[var(--text-secondary)] leading-relaxed text-sm sm:text-base">
          {/* Section 1 */}
          <section className="space-y-3">
            <h2 className="text-lg sm:text-xl font-bold text-[var(--text-primary)] flex items-center space-x-2">
              <Lock className="w-5 h-5 text-[var(--accent)]" />
              <span>1. Zero Personal Data Collection</span>
            </h2>
            <p>
              come on does not require you to create an account, log in, or provide any personal information (such as your name, email address, or phone number) to download public media. We do not maintain user profiles, tracking pixels, or third-party advertising cookies.
            </p>
          </section>

          {/* Section 2 */}
          <section className="space-y-3">
            <h2 className="text-lg sm:text-xl font-bold text-[var(--text-primary)] flex items-center space-x-2">
              <Trash2 className="w-5 h-5 text-red-500" />
              <span>2. Temporary Processing & Immediate File Purge</span>
            </h2>
            <p>
              When a download is requested, come on streams the media directly through a temporary server workspace solely to format and serve the file to your browser. 
            </p>
            <ul className="list-disc pl-6 space-y-1.5 text-xs sm:text-sm">
              <li>Temporary stream directories are automatically deleted immediately after transfer.</li>
              <li>We do not retain, archive, index, or distribute any downloaded media files.</li>
              <li>No database of downloaded media content is created or maintained.</li>
            </ul>
          </section>

          {/* Section 3 */}
          <section className="space-y-3">
            <h2 className="text-lg sm:text-xl font-bold text-[var(--text-primary)] flex items-center space-x-2">
              <Globe className="w-5 h-5 text-blue-500" />
              <span>3. Permitted & Lawful Use Policy</span>
            </h2>
            <p>
              come on is designed strictly for downloading public videos, your own created content, public domain videos, or media for which you have explicit rights or permissions.
            </p>
            <div className="p-4 rounded-xl bg-black/[0.02] border border-[var(--border-color)] text-xs sm:text-sm space-y-1">
              <p className="font-semibold text-[var(--text-primary)]">Strict Enforcement:</p>
              <p>
                come on strictly refuses and contains no mechanisms to bypass Digital Rights Management (DRM), private/unlisted protections, password-protected videos, or access control mechanisms.
              </p>
            </div>
          </section>

          {/* Section 4 */}
          <section className="space-y-3">
            <h2 className="text-lg sm:text-xl font-bold text-[var(--text-primary)] flex items-center space-x-2">
              <FileText className="w-5 h-5 text-purple-500" />
              <span>4. Network Security & SSRF Protection</span>
            </h2>
            <p>
              To maintain system integrity and prevent Server-Side Request Forgery (SSRF), all incoming URLs are validated against strict IP address blacklists and internal network filters. Requests targeting loopback, private intranet addresses, or cloud metadata endpoints are immediately rejected.
            </p>
          </section>

          {/* Section 5 */}
          <section className="space-y-3">
            <h2 className="text-lg sm:text-xl font-bold text-[var(--text-primary)]">
              5. Changes to This Policy
            </h2>
            <p>
              Any updates to this privacy policy will be posted directly to this page with an updated revision date. Continued use of Velora signifies your acceptance of these terms.
            </p>
          </section>
        </div>

        {/* Bottom CTA */}
        <div className="mt-16 pt-8 border-t border-[var(--border-color)] text-center">
          <Link
            href="/"
            className="inline-flex items-center space-x-2 px-6 py-3 rounded-xl bg-[var(--text-primary)] text-[var(--bg-surface)] font-medium text-sm hover:opacity-90 transition-all shadow-xs"
          >
            <span>Return to Downloader</span>
          </Link>
        </div>
      </main>

      <Footer />
    </div>
  );
}
