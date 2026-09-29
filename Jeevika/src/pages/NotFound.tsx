import React from 'react';
import { Link } from 'react-router-dom';
import { Compass, Home } from 'lucide-react';
import { Button } from '../components/ui/Button';

export const NotFound: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] p-6 text-center space-y-4">
      <div className="flex h-16 w-16 items-center justify-center rounded-3xl bg-brand-100 text-brand-700">
        <Compass className="h-8 w-8 animate-spin" />
      </div>
      <h1 className="text-3xl font-extrabold text-slate-900">404 - Page Not Found</h1>
      <p className="text-sm text-slate-500 max-w-sm">
        The route you are trying to access does not exist in the Phase 1 web application.
      </p>
      <Link to="/">
        <Button variant="default" size="default" className="gap-2 font-bold mt-2">
          <Home className="h-4 w-4" />
          <span>Return to Landing Page</span>
        </Button>
      </Link>
    </div>
  );
};
