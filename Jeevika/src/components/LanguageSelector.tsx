import React from 'react';
import { Globe } from 'lucide-react';
import { SUPPORTED_LANGUAGES } from '../lib/constants';
import { useLanguage } from '../hooks/useLanguage';
import { SupportedLanguage } from '../types';

interface LanguageSelectorProps {
  variant?: 'compact' | 'full';
  className?: string;
}

export const LanguageSelector: React.FC<LanguageSelectorProps> = ({
  variant = 'compact',
  className = '',
}) => {
  const { language, changeLanguage } = useLanguage();

  if (variant === 'full') {
    return (
      <div className={`grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3 ${className}`}>
        {SUPPORTED_LANGUAGES.map((lang) => (
          <button
            key={lang.code}
            onClick={() => changeLanguage(lang.code as SupportedLanguage)}
            className={`flex flex-col items-start p-4 rounded-xl border text-left transition-all ${
              language === lang.code
                ? 'border-brand-600 bg-brand-50 text-brand-900 ring-2 ring-brand-500/20 shadow-sm'
                : 'border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50 text-slate-800'
            }`}
          >
            <span className="text-lg font-bold text-slate-900">{lang.nameNative}</span>
            <span className="text-xs text-slate-500">{lang.nameEnglish}</span>
            <span className="text-[10px] text-slate-400 mt-2">{lang.region}</span>
          </button>
        ))}
      </div>
    );
  }

  return (
    <div className={`relative inline-flex items-center gap-1.5 ${className}`}>
      <Globe className="h-4 w-4 text-slate-500" />
      <select
        value={language}
        onChange={(e) => changeLanguage(e.target.value as SupportedLanguage)}
        className="bg-white/80 backdrop-blur-sm border border-slate-200 rounded-lg px-2.5 py-1 text-xs font-semibold text-slate-700 shadow-sm focus:outline-none focus:ring-2 focus:ring-brand-500 cursor-pointer hover:bg-white"
        aria-label="Select preferred language"
      >
        {SUPPORTED_LANGUAGES.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.nameNative} ({lang.nameEnglish})
          </option>
        ))}
      </select>
    </div>
  );
};
