'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';

interface HumaniserFormProps {
  inputText: string;
  mode: 'sales' | 'journalist';
  isLoading: boolean;
  onInputChange: (text: string) => void;
  onModeChange: (mode: 'sales' | 'journalist') => void;
  onSubmit: () => void;
  onClear: () => void;
}

export function HumaniserForm({
  inputText,
  mode,
  isLoading,
  onInputChange,
  onModeChange,
  onSubmit,
  onClear,
}: HumaniserFormProps) {
  const wordCount = inputText.trim().split(/\s+/).filter(Boolean).length;
  const charCount = inputText.length;

  return (
    <Card className="shadow-lg">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Input Text</CardTitle>
            <CardDescription>Paste your AI-generated text below</CardDescription>
          </div>
          <Badge variant="secondary" className="text-sm">
            {wordCount} words · {charCount} characters
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Mode Selector */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-slate-700 dark:text-slate-300">
            Output Style
          </label>
          <Tabs value={mode} onValueChange={(value) => onModeChange(value as 'sales' | 'journalist')}>
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="sales" disabled={isLoading}>
                Sales / Marketing
              </TabsTrigger>
              <TabsTrigger value="journalist" disabled={isLoading}>
                Journalist / Editorial
              </TabsTrigger>
            </TabsList>
          </Tabs>
        </div>

        {/* Text Input */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-slate-700 dark:text-slate-300">
            AI-Generated Text
          </label>
          <Textarea
            placeholder="Furthermore, it is important to note that our product offers exceptional value. Moreover, the features included are comprehensive and well-designed..."
            value={inputText}
            onChange={(e) => onInputChange(e.target.value)}
            disabled={isLoading}
            className="min-h-[300px] resize-y"
          />
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Minimum 20 characters required
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3">
          <Button
            onClick={onSubmit}
            disabled={isLoading || !inputText.trim() || inputText.trim().length < 20}
            className="flex-1"
            size="lg"
          >
            {isLoading ? (
              <>
                <svg
                  className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Humanising...
              </>
            ) : (
              'Humanise Text'
            )}
          </Button>
          <Button
            onClick={onClear}
            disabled={isLoading || !inputText}
            variant="outline"
            size="lg"
          >
            Clear
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
