import { useEffect, useState } from 'react';
import { useAppStore } from '../stores/useAppStore';
import { SupportedLanguage } from '../types';

type TranslationMap = Record<string, string>;

export function useLanguage() {
  const { language, setLanguage } = useAppStore();
  const [translations, setTranslations] = useState<TranslationMap>({});
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    setIsLoading(true);
    // Load locale JSON file with English fallback
    fetch(`/locales/${language}.json`)
      .then((res) => {
        if (!res.ok) throw new Error('Locale file not found');
        return res.json();
      })
      .then((data) => {
        setTranslations(data);
        setIsLoading(false);
      })
      .catch(() => {
        // Fallback to en.json if specified language file is missing
        fetch('/locales/en.json')
          .then((res) => res.json())
          .then((data) => {
            setTranslations(data);
            setIsLoading(false);
          });
      });
  }, [language]);

  const t = (key: string, fallback?: string): string => {
    return translations[key] || fallback || key;
  };

  const changeLanguage = (lang: SupportedLanguage) => {
    setLanguage(lang);
  };

  return {
    language,
    changeLanguage,
    t,
    isLoading,
  };
}
