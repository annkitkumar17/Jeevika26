import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Mic, LayoutDashboard, UserCheck, Eye } from 'lucide-react';
import { LanguageSelector } from './LanguageSelector';
import { DemoDataBadge } from './DemoDataBadge';
import { OfflineStatus } from './OfflineStatus';
import { Button } from './ui/Button';

export const PublicNavbar: React.FC = () => {
  const location = useLocation();

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200/80 bg-white/90 backdrop-blur-md shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2.5 transition-transform hover:scale-[1.01]">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand-700 text-white font-extrabold shadow-md shadow-brand-700/20">
            <Mic className="h-5 w-5 text-saffron-400" />
          </div>
          <div className="flex flex-col">
            <span className="font-extrabold text-base tracking-tight text-slate-900 leading-tight">
              Jeevika Saarthi <span className="text-brand-600">AI</span>
            </span>
            <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-widest">
              PM-AJAY Livelihood Assistant
            </span>
          </div>
        </Link>

        {/* Center / Navigation Links */}
        <nav className="hidden md:flex items-center gap-6 text-xs font-semibold text-slate-600">
          <Link
            to="/"
            className={`hover:text-brand-700 transition-colors ${
              location.pathname === '/' ? 'text-brand-700 font-bold' : ''
            }`}
          >
            How It Works
          </Link>
          <Link
            to="/recommendations"
            className={`hover:text-brand-700 transition-colors ${
              location.pathname === '/recommendations' ? 'text-brand-700 font-bold' : ''
            }`}
          >
            Sample Pathways
          </Link>
          <Link
            to="/facilitator"
            className={`hover:text-brand-700 transition-colors ${
              location.pathname === '/facilitator' ? 'text-brand-700 font-bold' : ''
            }`}
          >
            For Facilitators
          </Link>
          <Link
            to="/admin"
            className={`hover:text-brand-700 transition-colors ${
              location.pathname === '/admin' ? 'text-brand-700 font-bold' : ''
            }`}
          >
            District Insights
          </Link>
        </nav>

        {/* Right CTA & Controls */}
        <div className="flex items-center gap-3">
          <OfflineStatus className="hidden xl:inline-flex" />
          <LanguageSelector variant="compact" />
          <Link to="/onboarding">
            <Button variant="accent" size="sm" className="gap-1.5 font-bold shadow-sm">
              <Mic className="h-3.5 w-3.5" />
              <span>Voice Interview</span>
            </Button>
          </Link>
          <Link to="/dashboard" className="hidden sm:inline-flex">
            <Button variant="outline" size="sm" className="gap-1.5 text-xs">
              <LayoutDashboard className="h-3.5 w-3.5" />
              <span>Dashboard</span>
            </Button>
          </Link>
        </div>
      </div>
    </header>
  );
};
