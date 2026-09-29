import React, { useState } from 'react';
import { Mic, Square, AlertTriangle, Send } from 'lucide-react';
import { Button } from './ui/Button';
import { VoiceWaveform } from './VoiceWaveform';
import { useVoiceSession } from '../hooks/useVoiceSession';

interface VoiceRecorderProps {
  onRecorded: (transcriptText: string) => void;
  defaultSimulatedText?: string;
}

export const VoiceRecorder: React.FC<VoiceRecorderProps> = ({
  onRecorded,
  defaultSimulatedText = 'मैं सोलर पंप मरम्मत और बिजली फिटिंग का काम सीखना चाहता हूँ।',
}) => {
  const {
    isRecording,
    isProcessingASR,
    isSimulated,
    durationSeconds,
    permissionError,
    liveTranscript,
    startRecording,
    stopRecording,
    cancelRecording,
  } = useVoiceSession();

  const [typedInput, setTypedInput] = useState('');

  const handleStopAndSubmit = async () => {
    const transcript = await stopRecording('hi');
    const finalTranscript = transcript || liveTranscript.trim() || typedInput.trim() || defaultSimulatedText;
    onRecorded(finalTranscript);
  };

  const handleTypedSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (typedInput.trim()) {
      onRecorded(typedInput.trim());
      setTypedInput('');
    }
  };

  const formatTimer = (sec: number) => {
    const mins = Math.floor(sec / 60);
    const secs = sec % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  return (
    <div className="flex flex-col gap-4 p-4 rounded-2xl bg-white border border-slate-200 shadow-md">
      {permissionError && (
        <div className="flex items-center gap-2 p-3 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-xs">
          <AlertTriangle className="h-4 w-4 shrink-0 text-amber-600" />
          <span>{permissionError}</span>
        </div>
      )}

      {isRecording ? (
        <div className="flex flex-col items-center justify-center gap-4 py-6">
          <div className="flex items-center gap-3">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-rose-500"></span>
            </span>
            <span className="text-sm font-semibold text-slate-700">
              {isSimulated ? 'Simulated Recording' : 'Recording Audio'} ({formatTimer(durationSeconds)})
            </span>
          </div>

          <VoiceWaveform active={true} bars={24} height={48} colorClass="bg-rose-500" />

          {liveTranscript && (
            <div className="w-full max-w-md p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-800 text-center font-medium animate-fadeIn">
              <span className="text-brand-600 font-bold mr-1.5">Listening:</span>
              <span>"{liveTranscript}"</span>
            </div>
          )}

          {isProcessingASR && (
            <div className="text-xs text-brand-700 font-semibold flex items-center gap-2 animate-pulse">
              <span className="h-2 w-2 rounded-full bg-brand-600" />
              <span>Transcribing with Bhashini Indic ASR...</span>
            </div>
          )}

          <div className="flex items-center gap-3 mt-2">
            <Button variant="secondary" size="sm" onClick={cancelRecording}>
              Cancel
            </Button>
            <Button variant="destructive" size="default" onClick={handleStopAndSubmit} className="gap-2 shadow-md">
              <Square className="h-4 w-4 fill-white" />
              <span>Stop & Send</span>
            </Button>
          </div>
        </div>
      ) : (
        <div className="flex flex-col md:flex-row items-center gap-4 justify-between">
          <div className="w-full md:w-auto flex justify-center">
            <Button
              variant="accent"
              size="xl"
              onClick={() => startRecording('hi-IN')}
              className="w-full md:w-auto gap-3 text-slate-900 shadow-lg"
            >
              <Mic className="h-6 w-6 text-slate-900 animate-pulse" />
              <span>Tap to Speak / Record</span>
            </Button>
          </div>

          <div className="text-xs text-slate-400 text-center font-medium uppercase tracking-wider">OR</div>

          <form onSubmit={handleTypedSubmit} className="flex-1 w-full flex items-center gap-2">
            <input
              type="text"
              value={typedInput}
              onChange={(e) => setTypedInput(e.target.value)}
              placeholder="Type your answer in Hindi / English..."
              className="flex-1 px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
            />
            <Button type="submit" variant="default" size="default" disabled={!typedInput.trim()}>
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </div>
      )}
    </div>
  );
};
