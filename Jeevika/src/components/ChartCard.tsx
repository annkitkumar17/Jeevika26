import React from 'react';
import ReactECharts from 'echarts-for-react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/Card';
import { DemoDataBadge } from './DemoDataBadge';

interface ChartCardProps {
  title: string;
  subtitle?: string;
  option: any;
  height?: string;
  className?: string;
}

export const ChartCard: React.FC<ChartCardProps> = ({
  title,
  subtitle,
  option,
  height = '320px',
  className = '',
}) => {
  return (
    <Card className={`p-5 bg-white border-slate-200 ${className}`}>
      <CardHeader className="p-0 mb-4 flex flex-row items-center justify-between">
        <div>
          <CardTitle className="text-base font-bold text-slate-900">{title}</CardTitle>
          {subtitle && <p className="text-xs text-slate-500 mt-0.5">{subtitle}</p>}
        </div>
        <DemoDataBadge text="Analytics demo" className="py-0.5 px-2 text-[10px]" />
      </CardHeader>
      <CardContent className="p-0">
        <ReactECharts option={option} style={{ height, width: '100%' }} />
      </CardContent>
    </Card>
  );
};
