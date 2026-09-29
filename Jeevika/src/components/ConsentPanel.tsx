import React from 'react';
import { ShieldCheck, Info } from 'lucide-react';
import { Switch } from './ui/Switch';
import { Button } from './ui/Button';
import { useAppStore } from '../stores/useAppStore';

interface ConsentPanelProps {
  onConsentAccepted: () => void;
  className?: string;
}

export const ConsentPanel: React.FC<ConsentPanelProps> = ({
  onConsentAccepted,
  className = '',
}) => {
  const { consent, setConsent, completeConsent } = useAppStore();

  const isAllRequiredChecked = consent.profileCreation && consent.recommendations;

  const handleContinue = () => {
    if (isAllRequiredChecked) {
      completeConsent();
      onConsentAccepted();
    }
  };

  return (
    <div className={`p-6 rounded-2xl bg-white border border-slate-200 shadow-md ${className}`}>
      <div className="flex items-start gap-3 mb-4">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-brand-100 text-brand-800">
          <ShieldCheck className="h-6 w-6 text-brand-700" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-slate-900">Demographic & Voice Data Consent</h3>
          <p className="text-xs text-slate-500 mt-0.5">
            PM-AJAY GIA Component Livelihood Discovery Protocol (Phase 1 Local Prototype)
          </p>
        </div>
      </div>

      <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100 text-xs text-slate-700 space-y-2 mb-6">
        <div className="flex items-center gap-1.5 font-semibold text-slate-900">
          <Info className="h-4 w-4 text-brand-600" />
          <span>Demo Data Transparency Disclaimer:</span>
        </div>
        <p>
          This Phase 1 web interface runs entirely on your local browser using fictional mock beneficiary records. No personal data or Aadhaar information is transmitted to external servers.
        </p>
      </div>

      <div className="space-y-4 mb-6">
        <div className="flex items-center justify-between p-3.5 rounded-xl border border-slate-200 bg-slate-50/50">
          <div>
            <div className="text-sm font-bold text-slate-900">1. Local Profile Creation (Required)</div>
            <div className="text-xs text-slate-500">
              Allow local storage of voice interview responses to extract skill profile.
            </div>
          </div>
          <Switch
            checked={consent.profileCreation}
            onCheckedChange={(val) => setConsent({ profileCreation: val })}
            id="consent-profile"
          />
        </div>

        <div className="flex items-center justify-between p-3.5 rounded-xl border border-slate-200 bg-slate-50/50">
          <div>
            <div className="text-sm font-bold text-slate-900">2. NSQF Pathway Match (Required)</div>
            <div className="text-xs text-slate-500">
              Allow matching profile against seeded PMKK / JSS qualification packs.
            </div>
          </div>
          <Switch
            checked={consent.recommendations}
            onCheckedChange={(val) => setConsent({ recommendations: val })}
            id="consent-recommendations"
          />
        </div>

        <div className="flex items-center justify-between p-3.5 rounded-xl border border-slate-200 bg-slate-50/50">
          <div>
            <div className="text-sm font-bold text-slate-900">3. Facilitator Follow-up (Optional)</div>
            <div className="text-xs text-slate-500">
              Simulate referral notification to district VLE facilitator.
            </div>
          </div>
          <Switch
            checked={consent.followUp}
            onCheckedChange={(val) => setConsent({ followUp: val })}
            id="consent-followup"
          />
        </div>
      </div>

      <div className="flex justify-end">
        <Button
          variant="default"
          size="lg"
          disabled={!isAllRequiredChecked}
          onClick={handleContinue}
          className="w-full sm:w-auto font-bold px-8 shadow-md"
        >
          {isAllRequiredChecked ? 'Accept & Continue to Interview' : 'Please check required consents'}
        </Button>
      </div>
    </div>
  );
};
