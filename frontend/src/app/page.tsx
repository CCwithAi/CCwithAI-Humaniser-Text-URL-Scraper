'use client';

import { useState } from 'react';
import { useHumaniser } from '@/hooks/use-humaniser';
import { HumaniserForm } from '@/components/humaniser-form';
import { OutputDisplay } from '@/components/output-display';
import { MetricsDisplay } from '@/components/metrics-display';
import { UrlScraperForm } from '@/components/url-scraper-form';
import { Toaster } from '@/components/ui/toaster';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

export default function Home() {
  const {
    inputText,
    mode,
    isLoading,
    error,
    result,
    setInputText,
    setMode,
    humanise,
    reset,
    clearResult,
    copyToClipboard,
  } = useHumaniser();

  const [activeTab, setActiveTab] = useState('humanise');

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold tracking-tight text-slate-900 dark:text-slate-100 mb-2">
            AI Humaniser
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            Transform AI-generated text into authentic human writing
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-7xl mx-auto space-y-8">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full max-w-md mx-auto grid-cols-2">
              <TabsTrigger value="humanise">Humanise Text</TabsTrigger>
              <TabsTrigger value="scraper">Add Training Data</TabsTrigger>
            </TabsList>

            <TabsContent value="humanise" className="space-y-8">
              {/* Input Form */}
              <HumaniserForm
                inputText={inputText}
                mode={mode}
                isLoading={isLoading}
                onInputChange={setInputText}
                onModeChange={setMode}
                onSubmit={humanise}
                onClear={reset}
              />

          {/* Error Display */}
          {error && !result && (
            <div className="rounded-lg bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-900 p-4">
              <div className="flex items-start gap-3">
                <svg
                  className="h-5 w-5 text-red-600 dark:text-red-400 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <div>
                  <h3 className="text-sm font-medium text-red-800 dark:text-red-200">
                    Error
                  </h3>
                  <p className="text-sm text-red-700 dark:text-red-300 mt-1">
                    {error}
                  </p>
                </div>
              </div>
            </div>
          )}

              {/* Results Grid */}
              {result && (
                <div className="grid lg:grid-cols-3 gap-6">
                  <div className="lg:col-span-2">
                    <OutputDisplay
                      result={result}
                      onCopy={copyToClipboard}
                      onClear={clearResult}
                    />
                  </div>
                  <div>
                    <MetricsDisplay
                      metrics={result.metrics}
                      qualityScore={result.quality_score}
                    />
                  </div>
                </div>
              )}
            </TabsContent>

            <TabsContent value="scraper" className="space-y-8">
              <UrlScraperForm />

              <div className="rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 p-6">
                <h3 className="font-semibold text-slate-900 dark:text-slate-100 mb-2">
                  Why Add Training Data?
                </h3>
                <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                  <li className="flex gap-2">
                    <span className="text-green-600 dark:text-green-400">✓</span>
                    <span>More human examples = better output quality</span>
                  </li>
                  <li className="flex gap-2">
                    <span className="text-green-600 dark:text-green-400">✓</span>
                    <span>The system learns from real human writing styles</span>
                  </li>
                  <li className="flex gap-2">
                    <span className="text-green-600 dark:text-green-400">✓</span>
                    <span>Diverse examples help bypass AI detection tools</span>
                  </li>
                  <li className="flex gap-2">
                    <span className="text-green-600 dark:text-green-400">✓</span>
                    <span>Target: 50-100 examples for optimal results</span>
                  </li>
                </ul>
              </div>
            </TabsContent>
          </Tabs>
        </div>

        {/* Footer */}
        <footer className="mt-16 text-center text-sm text-slate-500 dark:text-slate-400">
          <p>
            Powered by ARCHON multi-agent system · GPT-4o-mini + Claude Sonnet 4
          </p>
        </footer>
      </div>

      {/* Toast Notifications */}
      <Toaster />
    </main>
  );
}
