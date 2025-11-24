'use client';

import { useState } from 'react';
import { scrapeAndIndexUrl, type ScrapeRequest } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2, Link as LinkIcon, CheckCircle2 } from 'lucide-react';

export function UrlScraperForm() {
  const { toast } = useToast();
  const [url, setUrl] = useState('');
  const [contentType, setContentType] = useState<'sales' | 'journalist'>('journalist');
  const [description, setDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<{ success: boolean; message: string; wordCount: number; filename: string } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validation
    if (!url.trim()) {
      toast({
        title: 'Validation Error',
        description: 'Please enter a URL',
        variant: 'destructive',
      });
      return;
    }

    if (!description.trim() || description.trim().length < 5) {
      toast({
        title: 'Validation Error',
        description: 'Description must be at least 5 characters long',
        variant: 'destructive',
      });
      return;
    }

    setIsLoading(true);
    setResult(null);

    try {
      const request: ScrapeRequest = {
        url: url.trim(),
        content_type: contentType,
        description: description.trim(),
      };

      const response = await scrapeAndIndexUrl(request);

      setResult({
        success: response.success,
        message: response.message,
        wordCount: response.word_count,
        filename: response.filename,
      });

      toast({
        title: 'Success!',
        description: `Scraped and indexed ${response.word_count} words from URL`,
      });

      // Clear form on success
      setUrl('');
      setDescription('');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An unexpected error occurred';

      toast({
        title: 'Error',
        description: errorMessage,
        variant: 'destructive',
      });

      setResult({
        success: false,
        message: errorMessage,
        wordCount: 0,
        filename: '',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setUrl('');
    setDescription('');
    setContentType('journalist');
    setResult(null);
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <LinkIcon className="h-5 w-5" />
          Add Training Data from URL
        </CardTitle>
        <CardDescription>
          Scrape content from any webpage and add it to the training database. This helps improve
          the quality of humanized text.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* URL Input */}
          <div className="space-y-2">
            <Label htmlFor="url">URL</Label>
            <Input
              id="url"
              type="url"
              placeholder="https://example.com/article"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              disabled={isLoading}
              className="font-mono text-sm"
            />
            <p className="text-xs text-muted-foreground">
              Enter the URL of an article, blog post, or webpage with quality human-written content
            </p>
          </div>

          {/* Content Type Select */}
          <div className="space-y-2">
            <Label htmlFor="content-type">Content Type</Label>
            <Select
              value={contentType}
              onValueChange={(value) => setContentType(value as 'sales' | 'journalist')}
              disabled={isLoading}
            >
              <SelectTrigger id="content-type">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="journalist">Journalist / Editorial</SelectItem>
                <SelectItem value="sales">Sales / Marketing</SelectItem>
              </SelectContent>
            </Select>
            <p className="text-xs text-muted-foreground">
              Select the type that best matches the content
            </p>
          </div>

          {/* Description Textarea */}
          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              placeholder="e.g., Food article about marshmallow recipes, Tech news about data breach, Sales email for SaaS product..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={isLoading}
              rows={3}
              className="resize-none"
            />
            <p className="text-xs text-muted-foreground">
              Brief description to help with indexing and retrieval (5-200 characters)
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-2">
            <Button type="submit" disabled={isLoading} className="flex-1">
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Scraping...
                </>
              ) : (
                'Scrape and Index'
              )}
            </Button>
            {!isLoading && (url || description) && (
              <Button type="button" variant="outline" onClick={handleReset}>
                Clear
              </Button>
            )}
          </div>

          {/* Result Display */}
          {result && (
            <div
              className={`mt-4 rounded-lg border p-4 ${
                result.success
                  ? 'border-green-200 bg-green-50 dark:border-green-800 dark:bg-green-950'
                  : 'border-red-200 bg-red-50 dark:border-red-800 dark:bg-red-950'
              }`}
            >
              <div className="flex items-start gap-2">
                {result.success ? (
                  <CheckCircle2 className="h-5 w-5 text-green-600 dark:text-green-400 mt-0.5" />
                ) : (
                  <div className="h-5 w-5 rounded-full border-2 border-red-600 dark:border-red-400 flex items-center justify-center mt-0.5">
                    <span className="text-red-600 dark:text-red-400 text-xs font-bold">!</span>
                  </div>
                )}
                <div className="flex-1">
                  <p className={result.success ? 'text-green-900 dark:text-green-100' : 'text-red-900 dark:text-red-100'}>
                    {result.message}
                  </p>
                  {result.success && (
                    <div className="mt-2 text-sm text-green-800 dark:text-green-200">
                      <p>Saved as: {result.filename}</p>
                      <p>Word count: {result.wordCount.toLocaleString()}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </form>
      </CardContent>
    </Card>
  );
}
