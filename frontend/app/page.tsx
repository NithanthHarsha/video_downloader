'use client';

import React, { useState } from 'react';
import { Navbar } from '../components/Navbar';
import { Hero } from '../components/Hero';
import { UrlInput } from '../components/UrlInput';
import { VideoPreview } from '../components/VideoPreview';
import { SuccessState } from '../components/SuccessState';
import { ErrorState } from '../components/ErrorState';
import { HowItWorks } from '../components/HowItWorks';
import { FeatureSection } from '../components/FeatureSection';
import { Footer } from '../components/Footer';
import { VideoInfo, DownloadStatus, ApiError, ProcessingState } from '../lib/types';
import { fetchVideoInfo, processAndDownloadVideo } from '../lib/api';

export default function Home() {
  const [state, setState] = useState<ProcessingState>('idle');
  const [videoInfo, setVideoInfo] = useState<VideoInfo | null>(null);
  const [downloadStatus, setDownloadStatus] = useState<DownloadStatus | null>(null);
  const [error, setError] = useState<ApiError | null>(null);

  const handleAnalyze = async (url: string) => {
    setState('fetching_info');
    setError(null);

    const res = await fetchVideoInfo(url);
    if (res.success && res.data) {
      setVideoInfo(res.data);
      setState('preview');
    } else {
      setError(res.error || { code: 'UNKNOWN_ERROR', message: 'Unable to analyze this video URL.' });
      setState('error');
    }
  };

  const handleStartDownload = async (formatId: string) => {
    if (!videoInfo) return;

    setState('downloading');
    setError(null);
    setDownloadStatus({
      task_id: 'direct-stream',
      status: 'downloading',
      progress: 50.0,
      eta_str: 'Processing...',
      speed_str: null,
      filename: null,
      filesize: null,
      filesize_str: null,
      download_url: null,
      error_message: null
    });

    const res = await processAndDownloadVideo(videoInfo.url, formatId);

    if (res.success && res.filename) {
      setDownloadStatus({
        task_id: 'completed',
        status: 'ready',
        progress: 100.0,
        filename: res.filename,
        download_url: res.blobUrl || '#',
        speed_str: null,
        eta_str: null,
        filesize: null,
        filesize_str: null,
        error_message: null
      });
      setState('ready');
    } else {
      setError(res.error || { code: 'DOWNLOAD_FAILED', message: 'Could not complete download process.' });
      setState('error');
    }
  };

  const handleReset = () => {
    setState('idle');
    setVideoInfo(null);
    setDownloadStatus(null);
    setError(null);
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />

      <main className="flex-1">
        <Hero />

        <div className="pb-16 px-4">
          {/* State 1 & 2: URL Input or Loading */}
          {(state === 'idle' || state === 'fetching_info') && (
            <UrlInput
              onAnalyze={handleAnalyze}
              isLoading={state === 'fetching_info'}
            />
          )}

          {/* State 3, 4 & 5: Video Preview & Downloading */}
          {(state === 'preview' || state === 'preparing' || state === 'downloading') && videoInfo && (
            <VideoPreview
              video={videoInfo}
              state={state}
              downloadStatus={downloadStatus}
              onStartDownload={handleStartDownload}
              onReset={handleReset}
            />
          )}

          {/* State 6: Download Ready / Success */}
          {state === 'ready' && downloadStatus && (
            <div className="max-w-2xl mx-auto">
              <SuccessState status={downloadStatus} onReset={handleReset} />
            </div>
          )}

          {/* State 7: Error State */}
          {state === 'error' && (
            <div className="max-w-2xl mx-auto">
              <ErrorState error={error} onRetry={handleReset} />
            </div>
          )}
        </div>

        <HowItWorks />
        <FeatureSection />
      </main>

      <Footer />
    </div>
  );
}
