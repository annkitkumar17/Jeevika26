import React from 'react';
import { cn } from '../../lib/utils';

interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value: number; // 0 to 100
  indicatorColor?: string;
}

export const Progress: React.FC<ProgressProps> = ({
  value,
  indicatorColor = 'bg-brand-600',
  className,
  ...props
}) => {
  const clampedValue = Math.min(100, Math.max(0, value));

  return (
    <div
      className={cn('relative h-2.5 w-full overflow-hidden rounded-full bg-slate-100', className)}
      {...props}
    >
      <div
        className={cn('h-full transition-all duration-500 ease-out rounded-full', indicatorColor)}
        style={{ width: `${clampedValue}%` }}
      />
    </div>
  );
};
