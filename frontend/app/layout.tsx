import type { Metadata, Viewport } from 'next';
import { DM_Sans } from 'next/font/google';
import './globals.css';

const dmSans = DM_Sans({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700', '800'],
  variable: '--font-dm-sans',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'come on — Simple Video Downloader',
  description: 'Download permitted online videos in available quality with a simple, private and elegant interface.',
  keywords: ['video downloader', 'fast download', 'mp4 download', 'audio extractor', 'clean video tool', 'come on'],
  authors: [{ name: 'come on' }],
  openGraph: {
    title: 'come on — Simple Video Downloader',
    description: 'Download permitted online videos in available quality with a simple, private and elegant interface.',
    type: 'website',
    locale: 'en_US',
    siteName: 'come on',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'come on — Simple Video Downloader',
    description: 'Download permitted online videos in available quality with a simple, private and elegant interface.',
  },
  icons: {
    icon: '/favicon.ico',
  },
};

export const viewport: Viewport = {
  themeColor: '#F5F5F0',
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={dmSans.variable} suppressHydrationWarning>
      <body className={`${dmSans.className} min-h-screen flex flex-col bg-[var(--bg-primary)] text-[var(--text-primary)] selection:bg-[var(--accent)] selection:text-white transition-colors duration-300 font-sans`}>
        {children}
      </body>
    </html>
  );
}
