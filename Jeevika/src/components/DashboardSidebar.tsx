import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Compass,
  FileCheck,
  UserCheck,
  BarChart3,
  Home,
  RotateCcw,
  Mic,
  Moon,
  Sun,
  Shield,
} from 'lucide-react';
import { useAppStore } from '../stores/useAppStore';
import { DemoDataBadge } from './DemoDataBadge';
import { Button } from './ui/Button';

export const DashboardSidebar: React.FC<{ className?: string }> = ({ className = '' }) => {
  const location = useLocation();
  const { reducedMotion, setReducedMotion, resetEntireDemo } = useAppStore();

  const navItems = [
    { label: 'Beneficiary Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { label: 'Livelihood Recommendations', path: '/recommendations', icon: Compass },
    { label: 'Profile Review', path: '/profile-review', icon: FileCheck },
    { label: 'Facilitator Workspace', path: '/facilitator', icon: UserCheck },
    { label: 'District Analytics', path: '/admin', icon: BarChart3 },
  ];

  return (
    <aside className={`w-64 bg-slate-900 text-white flex flex-col justify-between p-4 border-r border-slate-800 ${className}`}>
      <div>
        <div className="flex items-center gap-2.5 pb-6 border-b border-slate-800 mb-6">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand-600 text-white font-bold">
            <Mic className="h-5 w-5 text-saffron-400" />
          </div>
          <div>
            <span className="font-extrabold text-sm text-white block">Jeevika Saarthi AI</span>
            <span className="text-[10px] text-brand-300 font-semibold uppercase">Phase 1 Web App</span>
          </div>
        </div>

        <div className="space-y-1">
          <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest px-3 mb-2">
            Navigation
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                  isActive
                    ? 'bg-brand-700 text-white shadow-md shadow-brand-700/20'
                    : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </div>
      </div>

      <div className="space-y-4 pt-4 border-t border-slate-800">
        <DemoDataBadge text="Phase 1 Localhost" className="w-full justify-center text-[10px]" />

        <div className="flex items-center justify-between px-2 text-xs text-slate-400">
          <span>Reduced Motion</span>
          <button
            onClick={() => setReducedMotion(!reducedMotion)}
            className={`px-2 py-1 rounded text-[11px] font-bold ${
              reducedMotion ? 'bg-saffron-500 text-slate-900' : 'bg-slate-800 text-slate-300'
            }`}
          >
            {reducedMotion ? 'ON' : 'OFF'}
          </button>
        </div>

        <Button
          variant="secondary"
          size="sm"
          onClick={() => {
            if (confirm('Reset demo state to default?')) {
              resetEntireDemo();
              window.location.href = '/';
            }
          }}
          className="w-full gap-2 text-xs bg-slate-800 text-slate-300 hover:bg-slate-700 border-none"
        >
          <RotateCcw className="h-3.5 w-3.5" />
          <span>Reset Demo Session</span>
        </Button>

        <Link to="/" className="flex items-center justify-center gap-1 text-xs text-slate-500 hover:text-slate-300 pt-1">
          <Home className="h-3.5 w-3.5" />
          <span>Return to Landing Page</span>
        </Link>
      </div>
    </aside>
  );
};
