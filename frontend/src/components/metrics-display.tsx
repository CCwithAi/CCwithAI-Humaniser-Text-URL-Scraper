'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import type { QualityMetrics } from '@/lib/api';

interface MetricsDisplayProps {
  metrics: QualityMetrics;
  qualityScore: number;
}

interface MetricItem {
  label: string;
  value: number;
  description: string;
  format: 'percentage' | 'number';
}

export function MetricsDisplay({ metrics, qualityScore }: MetricsDisplayProps) {
  const metricItems: MetricItem[] = [
    {
      label: 'Burstiness',
      value: metrics.burstiness,
      description: 'Sentence length variation (higher = more natural)',
      format: 'percentage',
    },
    {
      label: 'Lexical Diversity',
      value: metrics.lexical_diversity,
      description: 'Vocabulary richness (higher = more varied words)',
      format: 'percentage',
    },
    {
      label: 'Contraction Ratio',
      value: metrics.contraction_ratio,
      description: "Natural language usage (can't, won't, etc.)",
      format: 'percentage',
    },
  ];

  const getProgressColor = (value: number) => {
    if (value >= 0.7) return 'bg-green-500';
    if (value >= 0.5) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <Card className="shadow-lg">
      <CardHeader>
        <CardTitle>Quality Metrics</CardTitle>
        <CardDescription>
          Analysis of humanisation quality
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Overall Quality Score */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
              Overall Quality
            </span>
            <span className="text-2xl font-bold text-slate-900 dark:text-slate-100">
              {(qualityScore * 100).toFixed(0)}%
            </span>
          </div>
          <Progress
            value={qualityScore * 100}
            className="h-3"
          />
          <p className="text-xs text-slate-500 dark:text-slate-400">
            {qualityScore >= 0.8 ? 'Excellent' : qualityScore >= 0.6 ? 'Good' : 'Needs improvement'}
          </p>
        </div>

        {/* Individual Metrics */}
        <div className="space-y-4 pt-2 border-t border-slate-200 dark:border-slate-800">
          {metricItems.map((metric) => (
            <div key={metric.label} className="space-y-2">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                    {metric.label}
                  </span>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    {metric.description}
                  </p>
                </div>
                <span className="text-lg font-semibold text-slate-900 dark:text-slate-100">
                  {metric.format === 'percentage'
                    ? `${(metric.value * 100).toFixed(1)}%`
                    : metric.value.toFixed(2)}
                </span>
              </div>
              <div className="relative h-2 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-800">
                <div
                  className={`h-full transition-all ${getProgressColor(metric.value)}`}
                  style={{ width: `${metric.value * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 gap-4 pt-2 border-t border-slate-200 dark:border-slate-800">
          <div className="text-center p-3 rounded-lg bg-slate-50 dark:bg-slate-900">
            <p className="text-2xl font-bold text-slate-900 dark:text-slate-100">
              {metrics.word_count}
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Words
            </p>
          </div>
          <div className="text-center p-3 rounded-lg bg-slate-50 dark:bg-slate-900">
            <p className="text-2xl font-bold text-slate-900 dark:text-slate-100">
              {metrics.sentence_count}
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Sentences
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
