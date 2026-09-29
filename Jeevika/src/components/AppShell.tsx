import React from 'react';
import { useLocation } from 'react-router-dom';
import { PublicNavbar } from './PublicNavbar';
import { DashboardSidebar } from './DashboardSidebar';
import { useAppStore } from '../stores/useAppStore';

export const AppShell: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation();
  const { reducedMotion } = useAppStore();

  const isPublicRoute = ['/', '/onboarding'].includes(location.pathname);

  return (
    <div className={`min-h-screen flex flex-col bg-slate-50 text-slate-900 ${reducedMotion ? 'body-reduced-motion' : ''}`}>
      {isPublicRoute ? (
        <>
          <PublicNavbar />
          <main className="flex-1">{children}</main>
        </>
      ) : (
        <div className="flex flex-1 min-h-screen">
          <DashboardSidebar className="hidden lg:flex shrink-0" />
          <div className="flex-1 flex flex-col min-w-0">
            <PublicNavbar />
            <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto">{children}</main>
          </div>
        </div>
      )}
    </div>
  );
};
