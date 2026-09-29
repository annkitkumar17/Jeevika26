import React from 'react';
import { motion } from 'framer-motion';

interface VoiceWaveformProps {
  active?: boolean;
  bars?: number;
  height?: number;
  className?: string;
  colorClass?: string;
}

export const VoiceWaveform: React.FC<VoiceWaveformProps> = ({
  active = true,
  bars = 16,
  height = 40,
  className = '',
  colorClass = 'bg-brand-500',
}) => {
  return (
    <div
      className={`flex items-center justify-center gap-1.5 h-12 px-4 py-2 rounded-2xl bg-slate-900/5 backdrop-blur-sm ${className}`}
      style={{ height: `${height}px` }}
      aria-label="Voice audio waveform visualizer"
    >
      {Array.from({ length: bars }).map((_, index) => {
        const randomScale = active ? Math.random() * 0.8 + 0.2 : 0.15;
        return (
          <motion.span
            key={index}
            className={`w-1 rounded-full ${colorClass}`}
            animate={{
              scaleY: active ? [0.2, randomScale, 0.3, 1, 0.2] : 0.2,
            }}
            transition={{
              duration: active ? 0.8 : 0.2,
              repeat: active ? Infinity : 0,
              repeatType: 'reverse',
              delay: index * 0.05,
            }}
            style={{ height: '100%', transformOrigin: 'center' }}
          />
        );
      })}
    </div>
  );
};
