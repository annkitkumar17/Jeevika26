import React from 'react';
import { Sparkles } from 'lucide-react';

interface QuickReplyChipsProps {
  chips: string[];
  onSelect: (chipText: string) => void;
  className?: string;
}

export const QuickReplyChips: React.FC<QuickReplyChipsProps> = ({
  chips,
  onSelect,
  className = '',
}) => {
  if (!chips || chips.length === 0) return null;

  return (
    <div className={`flex flex-col gap-2 my-3 ${className}`}>
      <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-500">
        <Sparkles className="h-3.5 w-3.5 text-saffron-500" />
        <span>Suggested Quick Answers (Tap to select):</span>
      </div>
      <div className="flex flex-wrap gap-2">
        {chips.map((chip, idx) => (
          <button
            key={idx}
            onClick={() => onSelect(chip)}
            className="px-3 py-1.5 rounded-xl border border-slate-200 bg-white hover:border-brand-500 hover:bg-brand-50 text-slate-700 hover:text-brand-900 text-xs font-medium transition-all shadow-sm active:scale-95"
          >
            {chip}
          </button>
        ))}
      </div>
    </div>
  );
};
