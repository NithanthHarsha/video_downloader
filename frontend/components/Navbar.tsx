'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Menu, X, ShieldCheck } from 'lucide-react';

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header
      className={`sticky top-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-[#F5F5F0]/90 backdrop-blur-md border-b border-[var(--border-color)] py-3.5 shadow-xs'
          : 'bg-transparent py-5'
      }`}
    >
      <div className="max-w-5xl mx-auto px-6 sm:px-8 flex items-center justify-between">
        {/* Brand Logo */}
        <Link
          href="/"
          className="group flex items-center focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--accent)] rounded-xl py-0.5 transition-all"
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/logo.png"
            alt="Come on Logo"
            className="h-12 sm:h-16 md:h-20 w-auto object-contain drop-shadow-xs group-hover:scale-105 transition-transform duration-300"
          />
        </Link>

        {/* Desktop Navigation Links */}
        <nav className="hidden md:flex items-center space-x-8 text-sm font-medium text-[var(--text-secondary)]">
          <Link
            href="/#how-it-works"
            className="hover:text-[var(--text-primary)] transition-colors"
          >
            How it works
          </Link>
          <Link
            href="/features"
            className="hover:text-[var(--text-primary)] transition-colors"
          >
            Features
          </Link>
          <Link
            href="/privacy"
            className="hover:text-[var(--text-primary)] transition-colors flex items-center space-x-1"
          >
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
            <span>Privacy</span>
          </Link>
        </nav>

        {/* Mobile Navigation Toggle */}
        <div className="flex items-center space-x-3 md:hidden">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle Navigation Menu"
            className="p-2 rounded-lg text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-black/5 transition-colors"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-[var(--border-color)] bg-[#F5F5F0]/98 backdrop-blur-xl px-6 py-4 space-y-3 animate-in fade-in slide-in-from-top-2 duration-200">
          <Link
            href="/#how-it-works"
            onClick={() => setMobileMenuOpen(false)}
            className="block py-2 text-sm font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)]"
          >
            How it works
          </Link>
          <Link
            href="/features"
            onClick={() => setMobileMenuOpen(false)}
            className="block py-2 text-sm font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)]"
          >
            Features
          </Link>
          <Link
            href="/privacy"
            onClick={() => setMobileMenuOpen(false)}
            className="block py-2 text-sm font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)]"
          >
            Privacy & Policy
          </Link>
        </div>
      )}
    </header>
  );
}
