import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'sonner';

import { AppShell } from './components/AppShell';
import { Landing } from './pages/Landing';
import { Onboarding } from './pages/Onboarding';
import { Conversation } from './pages/Conversation';
import { ProfileReview } from './pages/ProfileReview';
import { Recommendations } from './pages/Recommendations';
import { PathwayDetail } from './pages/PathwayDetail';
import { Dashboard } from './pages/Dashboard';
import { Facilitator } from './pages/Facilitator';
import { Admin } from './pages/Admin';
import { NotFound } from './pages/NotFound';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppShell>
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/onboarding" element={<Onboarding />} />
            <Route path="/conversation" element={<Conversation />} />
            <Route path="/profile-review" element={<ProfileReview />} />
            <Route path="/recommendations" element={<Recommendations />} />
            <Route path="/pathway/:id" element={<PathwayDetail />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/facilitator" element={<Facilitator />} />
            <Route path="/admin" element={<Admin />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </AppShell>
        <Toaster position="top-right" richColors />
      </BrowserRouter>
    </QueryClientProvider>
  );
};

export default App;
