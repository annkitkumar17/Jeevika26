import React from 'react';
import { Database } from 'lucide-react';
import { Badge } from './ui/Badge';

export const DemoDataBadge: React.FC<{ className?: string; text?: string }> = ({
  className,
  text = 'Demo / locally seeded data',
}) => {
  return (
    <Badge
      variant="saffron"
      className={`inline-flex items-center gap-1.5 font-medium shadow-sm ${className}`}
    >
      <Database className="h-3 w-3 animate-pulse" />
      <span>{text}</span>
    </Badge>
  );
};
