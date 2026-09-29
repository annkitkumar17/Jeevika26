import { useState, useRef, useEffect, useCallback } from 'react';
import { apiClient } from '../services/apiClient';

export interface VoiceSessionState {
  isRecording: boolean;
  isProcessingASR: boolean;
  isSimulated: boolean;
  durationSeconds: number;
  audioBlob: Blob | null;
  audioUrl: string | null;
  hasPermission: boolean | null;
  permissionError: string | null;
  isPlayingQuestion: boolean;
  liveTranscript: string;
}

export function useVoiceSession() {
  const [state, setState] = useState<VoiceSessionState>({
    isRecording: false,
    isProcessingASR: false,
    isSimulated: false,
    durationSeconds: 0,
    audioBlob: null,
    audioUrl: null,
    hasPermission: null,
    permissionError: null,
    isPlayingQuestion: false,
    liveTranscript: '',
  });

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const recognitionRef = useRef<any>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const currentAudioElementRef = useRef<HTMLAudioElement | null>(null);

  // Check MediaRecorder availability
  useEffect(() => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      setState((prev) => ({
        ...prev,
        hasPermission: false,
        isSimulated: true,
        permissionError: 'Browser does not support microphone input. Using simulated voice mode.',
      }));
    }
  }, []);

  const startRecording = useCallback(async (lang: string = 'hi') => {
    audioChunksRef.current = [];
    setState((prev) => ({ ...prev, liveTranscript: '', isProcessingASR: false }));

    // Start Web Speech API SpeechRecognition if available for live interim feedback
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      try {
        const recognition = new SpeechRecognition();
        recognition.lang = lang === 'hi' ? 'hi-IN' : 'en-US';
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onresult = (event: any) => {
          let currentTranscript = '';
          for (let i = 0; i < event.results.length; i++) {
            currentTranscript += event.results[i][0].transcript;
          }
          setState((prev) => ({ ...prev, liveTranscript: currentTranscript }));
        };

        recognition.start();
        recognitionRef.current = recognition;
      } catch (err) {
        console.warn('SpeechRecognition initialization notice:', err);
      }
    }

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;

        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data);
          }
        };

        mediaRecorder.onstop = () => {
          const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
          const url = URL.createObjectURL(blob);
          setState((prev) => ({
            ...prev,
            isRecording: false,
            audioBlob: blob,
            audioUrl: url,
          }));
          stream.getTracks().forEach((track) => track.stop());
        };

        mediaRecorder.start();
        setState((prev) => ({
          ...prev,
          isRecording: true,
          isSimulated: false,
          durationSeconds: 0,
          hasPermission: true,
          permissionError: null,
        }));

        timerRef.current = setInterval(() => {
          setState((prev) => ({ ...prev, durationSeconds: prev.durationSeconds + 1 }));
        }, 1000);
      } catch (err: any) {
        startSimulatedRecording();
      }
    } else {
      startSimulatedRecording();
    }
  }, []);

  const startSimulatedRecording = useCallback(() => {
    setState((prev) => ({
      ...prev,
      isRecording: true,
      isSimulated: true,
      durationSeconds: 0,
      hasPermission: false,
      permissionError: 'Microphone permission disabled or unavailable. Operating in simulation mode.',
    }));

    timerRef.current = setInterval(() => {
      setState((prev) => ({ ...prev, durationSeconds: prev.durationSeconds + 1 }));
    }, 1000);
  }, []);

  const stopRecording = useCallback(async (lang: string = 'hi'): Promise<string> => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }

    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch {
        // ignore
      }
    }

    let recordedBlob: Blob | null = null;
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      if (audioChunksRef.current.length > 0) {
        recordedBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
      }
    } else {
      setState((prev) => ({
        ...prev,
        isRecording: false,
        audioUrl: 'simulated_audio_track',
      }));
    }

    // Try Bhashini ASR if blob exists
    if (recordedBlob && recordedBlob.size > 100) {
      try {
        setState((prev) => ({ ...prev, isProcessingASR: true }));
        const reader = new FileReader();
        const base64Promise = new Promise<string>((resolve) => {
          reader.onloadend = () => {
            const base64 = (reader.result as string).split(',')[1] || '';
            resolve(base64);
          };
          reader.readAsDataURL(recordedBlob!);
        });
        const base64Audio = await base64Promise;
        if (base64Audio) {
          const bhashiniRes = await apiClient.transcribeBhashini(base64Audio, lang);
          if (bhashiniRes?.success && bhashiniRes.transcript.trim()) {
            setState((prev) => ({ ...prev, isProcessingASR: false, liveTranscript: bhashiniRes.transcript }));
            return bhashiniRes.transcript.trim();
          }
        }
      } catch (err) {
        console.warn('Bhashini ASR pipeline note:', err);
      } finally {
        setState((prev) => ({ ...prev, isProcessingASR: false }));
      }
    }

    return state.liveTranscript.trim();
  }, [state.liveTranscript]);

  const cancelRecording = useCallback(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    if (recognitionRef.current) {
      try {
        recognitionRef.current.abort();
      } catch {
        // ignore
      }
    }
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
    audioChunksRef.current = [];
    setState((prev) => ({
      ...prev,
      isRecording: false,
      isProcessingASR: false,
      durationSeconds: 0,
      audioBlob: null,
      audioUrl: null,
      liveTranscript: '',
    }));
  }, []);

  const speakText = useCallback(async (text: string, lang = 'hi') => {
    if (currentAudioElementRef.current) {
      currentAudioElementRef.current.pause();
      currentAudioElementRef.current = null;
    }

    setState((prev) => ({ ...prev, isPlayingQuestion: true }));

    // 1. Try Bhashini Indic TTS
    try {
      const ttsRes = await apiClient.synthesizeBhashini(text, lang, 'female');
      if (ttsRes?.success && ttsRes.audio_base64) {
        const audio = new Audio(`data:audio/wav;base64,${ttsRes.audio_base64}`);
        currentAudioElementRef.current = audio;
        audio.onended = () => setState((prev) => ({ ...prev, isPlayingQuestion: false }));
        audio.onerror = () => speakBrowserFallback(text, lang);
        await audio.play();
        return;
      }
    } catch (err) {
      console.warn('Bhashini TTS note, using Web Speech synthesis:', err);
    }

    // 2. Web Speech API Synthesis Fallback
    speakBrowserFallback(text, lang);
  }, []);

  const speakBrowserFallback = (text: string, lang: string) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = lang === 'hi' ? 'hi-IN' : 'en-US';
      utterance.rate = 0.95;
      utterance.onstart = () => setState((prev) => ({ ...prev, isPlayingQuestion: true }));
      utterance.onend = () => setState((prev) => ({ ...prev, isPlayingQuestion: false }));
      utterance.onerror = () => setState((prev) => ({ ...prev, isPlayingQuestion: false }));
      window.speechSynthesis.speak(utterance);
    } else {
      setState((prev) => ({ ...prev, isPlayingQuestion: true }));
      setTimeout(() => {
        setState((prev) => ({ ...prev, isPlayingQuestion: false }));
      }, 2500);
    }
  };

  return {
    ...state,
    startRecording,
    stopRecording,
    cancelRecording,
    speakText,
  };
}
