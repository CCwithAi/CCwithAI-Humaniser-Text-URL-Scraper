'use client';

import { useState } from 'react';
import { humaniseText, type HumaniseRequest, type HumaniseResponse } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';

interface UseHumaniserState {
  inputText: string;
  mode: 'sales' | 'journalist';
  isLoading: boolean;
  error: string | null;
  result: HumaniseResponse | null;
}

export function useHumaniser() {
  const { toast } = useToast();
  const [state, setState] = useState<UseHumaniserState>({
    inputText: '',
    mode: 'sales',
    isLoading: false,
    error: null,
    result: null,
  });

  const setInputText = (text: string) => {
    setState((prev) => ({ ...prev, inputText: text, error: null }));
  };

  const setMode = (mode: 'sales' | 'journalist') => {
    setState((prev) => ({ ...prev, mode }));
  };

  const reset = () => {
    setState({
      inputText: '',
      mode: 'sales',
      isLoading: false,
      error: null,
      result: null,
    });
  };

  const clearResult = () => {
    setState((prev) => ({ ...prev, result: null, error: null }));
  };

  const humanise = async () => {
    // Validation
    if (!state.inputText.trim()) {
      setState((prev) => ({ ...prev, error: 'Please enter some text to humanise' }));
      toast({
        title: 'Validation Error',
        description: 'Please enter some text to humanise',
        variant: 'destructive',
      });
      return;
    }

    if (state.inputText.trim().length < 20) {
      setState((prev) => ({ ...prev, error: 'Text must be at least 20 characters long' }));
      toast({
        title: 'Validation Error',
        description: 'Text must be at least 20 characters long',
        variant: 'destructive',
      });
      return;
    }

    setState((prev) => ({ ...prev, isLoading: true, error: null, result: null }));

    try {
      const request: HumaniseRequest = {
        input_text: state.inputText,
        mode: state.mode,
      };

      const response = await humaniseText(request);

      setState((prev) => ({
        ...prev,
        isLoading: false,
        result: response,
        error: null,
      }));

      toast({
        title: 'Success!',
        description: `Text humanised successfully in ${response.iterations} iteration${response.iterations > 1 ? 's' : ''}`,
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An unexpected error occurred';

      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
        result: null,
      }));

      toast({
        title: 'Error',
        description: errorMessage,
        variant: 'destructive',
      });
    }
  };

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      toast({
        title: 'Copied!',
        description: 'Text copied to clipboard',
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to copy text to clipboard',
        variant: 'destructive',
      });
    }
  };

  return {
    inputText: state.inputText,
    mode: state.mode,
    isLoading: state.isLoading,
    error: state.error,
    result: state.result,
    setInputText,
    setMode,
    humanise,
    reset,
    clearResult,
    copyToClipboard,
  };
}
