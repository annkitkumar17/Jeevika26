import React from 'react';
import { CheckCircle2, Clock, Calendar, ChevronRight } from 'lucide-react';
import { Milestone } from '../types';

interface PathwayTimelineProps {
  milestones: Milestone[];
  currentStepIndex?: number;
  className?: string;
}

export const PathwayTimeline: React.FC<PathwayTimelineProps> = ({
  milestones,
  currentStepIndex = 0,
  className = '',
}) => {
  return (
    <div className={`relative pl-6 border-l-2 border-slate-200 space-y-6 ${className}`}>
      {milestones.map((milestone, index) => {
        const isCompleted = index < currentStepIndex;
        const isCurrent = index === currentStepIndex;

        return (
          <div key={index} className="relative group">
            {/* Timeline node icon */}
            <div
              className={`absolute -left-[31px] top-0 flex h-7 w-7 items-center justify-center rounded-full text-xs font-bold transition-all ${
                isCompleted
                  ? 'bg-emerald-600 text-white ring-4 ring-emerald-100'
                  : isCurrent
                  ? 'bg-brand-600 text-white ring-4 ring-brand-100 animate-pulse'
                  : 'bg-slate-200 text-slate-500'
              }`}
            >
              {isCompleted ? <CheckCircle2 className="h-4 w-4" /> : index + 1}
            </div>

            <div className="flex flex-col gap-1 bg-white p-4 rounded-xl border border-slate-200 shadow-sm transition-all group-hover:border-brand-300">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-slate-900 text-sm">{milestone.title}</span>
                <span className="inline-flex items-center gap-1 font-semibold text-brand-700 bg-brand-50 px-2 py-0.5 rounded-md text-[11px]">
                  <Calendar className="h-3 w-3" />
                  {milestone.duration}
                </span>
              </div>
              <p className="text-xs text-slate-600 mt-1 leading-relaxed">{milestone.description}</p>
              {isCurrent && (
                <div className="flex items-center gap-1 text-[11px] font-semibold text-brand-700 mt-2">
                  <Clock className="h-3 w-3" />
                  <span>Current Active Stage</span>
                  <ChevronRight className="h-3 w-3" />
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
