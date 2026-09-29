import React from 'react';
import { LucideIcon } from 'lucide-react';
import { Card } from './ui/Card';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: string;
  icon: LucideIcon;
  iconColorClass?: string;
  className?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  trend,
  icon: Icon,
  iconColorClass = 'bg-brand-100 text-brand-700',
  className = '',
}) => {
  return (
    <Card className={`flex items-start justify-between p-5 bg-white border-slate-200 shadow-sm ${className}`}>
      <div className="space-y-1">
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{title}</span>
        <div className="text-2xl font-extrabold text-slate-900 tracking-tight">{value}</div>
        {subtitle && <p className="text-xs text-slate-500 font-medium">{subtitle}</p>}
        {trend && (
          <span className="inline-block text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md mt-1">
            {trend}
          </span>
        )}
      </div>
      <div className={`p-3 rounded-xl ${iconColorClass}`}>
        <Icon className="h-6 w-6" />
      </div>
    </Card>
  );
};
