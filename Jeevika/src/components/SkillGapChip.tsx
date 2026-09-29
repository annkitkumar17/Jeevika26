import React from 'react';
import { Badge } from './ui/Badge';

export const SkillGapChip: React.FC<{ gapText: string }> = ({ gapText }) => {
  return (
    <Badge variant="outline" className="bg-slate-50 border-slate-200 text-slate-700 text-[11px] font-medium py-0.5 px-2">
      {gapText}
    </Badge>
  );
};
