import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '../../lib/utils';

const badgeVariants = cva(
  'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default: 'border-transparent bg-brand-100 text-brand-800 border border-brand-200',
        saffron: 'border-transparent bg-saffron-100 text-saffron-800 border border-saffron-200',
        success: 'border-transparent bg-emerald-100 text-emerald-800 border border-emerald-200',
        warning: 'border-transparent bg-amber-100 text-amber-800 border border-amber-200',
        destructive: 'border-transparent bg-rose-100 text-rose-800 border border-rose-200',
        outline: 'text-slate-700 border border-slate-300',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />;
}
