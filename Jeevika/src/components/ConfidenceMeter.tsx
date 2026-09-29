import React from 'react';
import { Sparkles } from 'lucide-react';
import { Progress } from './ui/Progress';
import { DemoDataBadge } from './DemoDataBadge';

interface ConfidenceMeterProps {
  score: number; // 0 to 100
  label?: string;
  className?: string;
}

export const ConfidenceMeter: React.FC<ConfidenceMeterProps> = ({
  score,
  label = 'AI Extraction Confidence',
  className = '',
}) => {
  return (
    <div className={`p-4 rounded-xl bg-slate-900 text-white shadow-md ${className}`}>
      <div className="flex items-center justify-between text-xs mb-2">
        <div className="flex items-center gap-1.5 font-semibold text-brand-300">
          <Sparkles className="h-4 w-4 text-saffron-400" />
          <span>{label}</span>
        </div>
        <span className="text-base font-bold text-saffron-400">{score}%</span>
      </div>
      <Progress value={score} indicatorColor="bg-saffron-500" className="bg-slate-800 h-2" />
      <div className="flex items-center justify-between mt-3 text-[11px] text-slate-400">
        <span>High precision NLP extraction</span>
        <DemoDataBadge text="Demo confidence" className="py-0 px-1 text-[10px]" />
      </div>
    </div>
  );
};
