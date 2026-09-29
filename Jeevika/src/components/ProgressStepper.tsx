import React from 'react';
import { Check } from 'lucide-react';
import { Progress } from './ui/Progress';

interface Step {
  title: string;
  description?: string;
}

interface ProgressStepperProps {
  steps: Step[];
  currentStepIndex: number;
  className?: string;
}

export const ProgressStepper: React.FC<ProgressStepperProps> = ({
  steps,
  currentStepIndex,
  className = '',
}) => {
  const percentage = Math.round(((currentStepIndex + 1) / steps.length) * 100);

  return (
    <div className={`flex flex-col gap-3 ${className}`}>
      <div className="flex items-center justify-between text-xs font-semibold text-slate-600">
        <span>
          Question {currentStepIndex + 1} of {steps.length}
        </span>
        <span className="text-brand-700 font-bold">{percentage}% Complete</span>
      </div>
      <Progress value={percentage} indicatorColor="bg-brand-600" />
      <div className="hidden sm:flex items-center justify-between text-[11px] text-slate-400 mt-1">
        {steps.map((step, idx) => (
          <div
            key={idx}
            className={`flex items-center gap-1 ${
              idx <= currentStepIndex ? 'text-brand-800 font-semibold' : ''
            }`}
          >
            <div
              className={`h-4 w-4 rounded-full flex items-center justify-center text-[9px] ${
                idx < currentStepIndex
                  ? 'bg-emerald-500 text-white'
                  : idx === currentStepIndex
                  ? 'bg-brand-600 text-white'
                  : 'bg-slate-200 text-slate-500'
              }`}
            >
              {idx < currentStepIndex ? <Check className="h-2.5 w-2.5" /> : idx + 1}
            </div>
            <span className="truncate max-w-[80px]">{step.title}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
