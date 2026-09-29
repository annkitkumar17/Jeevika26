import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Globe, ArrowRight } from 'lucide-react';
import { LanguageSelector } from '../components/LanguageSelector';
import { ConsentPanel } from '../components/ConsentPanel';
import { DemoDataBadge } from '../components/DemoDataBadge';
import { useLanguage } from '../hooks/useLanguage';

export const Onboarding: React.FC = () => {
  const navigate = useNavigate();
  const { t, language } = useLanguage();

  const handleConsentAccepted = () => {
    navigate('/conversation');
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 space-y-8">
      {/* HEADER */}
      <div className="text-center space-y-2">
        <DemoDataBadge text="Phase 1 Onboarding & Language Selection" />
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
          {t('consentTitle', 'Select Language & Give Consent')}
        </h1>
        <p className="text-sm text-slate-600 max-w-xl mx-auto">
          {t('consentSubtitle', 'Choose your preferred language for the voice interview and accept demo guidelines.')}
        </p>
      </div>

      {/* LANGUAGE SELECTOR GRID */}
      <div className="space-y-3">
        <div className="flex items-center gap-2 text-sm font-bold text-slate-800">
          <Globe className="h-4 w-4 text-brand-600" />
          <span>Preferred Interview Language:</span>
        </div>
        <LanguageSelector variant="full" />
      </div>

      {/* CONSENT FORM */}
      <ConsentPanel onConsentAccepted={handleConsentAccepted} />
    </div>
  );
};
