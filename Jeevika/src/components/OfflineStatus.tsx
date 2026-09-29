import React, { useEffect, useState } from 'react';
import { Wifi, WifiOff } from 'lucide-react';
import { Badge } from './ui/Badge';

export const OfflineStatus: React.FC<{ className?: string }> = ({ className = '' }) => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return (
    <div className={`inline-flex items-center gap-1.5 ${className}`}>
      {isOnline ? (
        <Badge variant="success" className="gap-1 text-[10px] py-0.5">
          <Wifi className="h-3 w-3 text-emerald-600" />
          <span>Localhost PWA Online</span>
        </Badge>
      ) : (
        <Badge variant="warning" className="gap-1 text-[10px] py-0.5 animate-pulse">
          <WifiOff className="h-3 w-3 text-amber-600" />
          <span>Offline Sync Mode</span>
        </Badge>
      )}
    </div>
  );
};
