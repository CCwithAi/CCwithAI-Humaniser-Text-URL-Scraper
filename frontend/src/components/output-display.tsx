'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import type { HumaniseResponse } from '@/lib/api';

interface OutputDisplayProps {
  result: HumaniseResponse;
  onCopy: (text: string) => void;
  onClear: () => void;
}

export function OutputDisplay({ result, onCopy, onClear }: OutputDisplayProps) {
  const wordCount = result.output_text.trim().split(/\s+/).filter(Boolean).length;
  const charCount = result.output_text.length;

  // Quality score color
  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600 dark:text-green-400';
    if (score >= 0.6) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getScoreBadge = (score: number) => {
    if (score >= 0.8) return 'default';
    if (score >= 0.6) return 'secondary';
    return 'destructive';
  };

  return (
    <Card className="shadow-lg border-2 border-green-200 dark:border-green-900">
      <CardHeader>
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <CardTitle className="flex items-center gap-2">
              Humanised Output
              <Badge variant={getScoreBadge(result.quality_score)}>
                Quality: {(result.quality_score * 100).toFixed(0)}%
              </Badge>
            </CardTitle>
            <CardDescription>
              Transformed in {result.iterations} iteration{result.iterations > 1 ? 's' : ''} ·
              {result.processing_time_ms}ms · {result.mode} mode
            </CardDescription>
          </div>
          <div className="text-right">
            <Badge variant="secondary" className="text-sm">
              {wordCount} words · {charCount} characters
            </Badge>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Output Text */}
        <div className="rounded-lg bg-slate-50 dark:bg-slate-900 p-6 border border-slate-200 dark:border-slate-800">
          <p className="text-slate-900 dark:text-slate-100 whitespace-pre-wrap leading-relaxed">
            {result.output_text}
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3">
          <Button
            onClick={() => onCopy(result.output_text)}
            className="flex-1"
            size="lg"
          >
            <svg
              className="mr-2 h-4 w-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
              />
            </svg>
            Copy to Clipboard
          </Button>
          <Button onClick={onClear} variant="outline" size="lg">
            Clear Output
          </Button>
        </div>

        {/* Download Option */}
        <Button
          onClick={() => {
            const blob = new Blob([result.output_text], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `humanised-${result.mode}-${Date.now()}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
          }}
          variant="ghost"
          className="w-full"
          size="sm"
        >
          <svg
            className="mr-2 h-4 w-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
            />
          </svg>
          Download as .txt
        </Button>
      </CardContent>
    </Card>
  );
}
