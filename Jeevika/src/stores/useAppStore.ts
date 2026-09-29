import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import {
  SupportedLanguage,
  ConsentState,
  BeneficiaryProfile,
  PathwayRecommendation,
  ChatMessage,
  GeoLocation,
} from '../types';

interface AppStore {
  // App domain
  language: SupportedLanguage;
  setLanguage: (lang: SupportedLanguage) => void;
  reducedMotion: boolean;
  setReducedMotion: (enabled: boolean) => void;
  demoMode: boolean;
  setDemoMode: (enabled: boolean) => void;

  // Consent domain
  consent: ConsentState;
  setConsent: (consentPartial: Partial<ConsentState>) => void;
  completeConsent: () => void;

  // Conversation domain
  currentQuestionIndex: number;
  answers: Record<string, string>;
  messages: ChatMessage[];
  interviewStatus: 'idle' | 'in_progress' | 'completed';
  setAnswer: (key: string, value: string) => void;
  addMessage: (msg: ChatMessage) => void;
  confirmMessage: (id: string) => void;
  editMessage: (id: string, newText: string) => void;
  nextQuestion: () => void;
  prevQuestion: () => void;
  resetConversation: () => void;

  // Beneficiary domain
  profile: BeneficiaryProfile | null;
  userLocation: GeoLocation | null;
  setProfile: (profile: BeneficiaryProfile) => void;
  setUserLocation: (loc: GeoLocation) => void;
  setEnrolledPathway: (pathwayId: string) => void;

  // Recommendations domain
  recommendations: PathwayRecommendation[];
  selectedPathwayId: string | null;
  savedPathwayIds: string[];
  setRecommendations: (items: PathwayRecommendation[]) => void;
  setSelectedPathwayId: (id: string | null) => void;
  toggleSavePathway: (id: string) => void;

  // UI domain
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  activeModal: string | null;
  setActiveModal: (modalId: string | null) => void;

  // Reset demo
  resetEntireDemo: () => void;
}

const initialConsent: ConsentState = {
  profileCreation: false,
  recommendations: false,
  followUp: false,
  completedAt: null,
};

const initialLocation: GeoLocation = {
  state: 'Uttar Pradesh',
  district: 'Lucknow',
  block: 'Sadar',
  village: 'Rampur Demo',
  latitude: 26.8467,
  longitude: 80.9462,
  dataStatus: 'demo_seeded',
};

export const useAppStore = create<AppStore>()(
  persist(
    (set, get) => ({
      // App state
      language: 'hi',
      setLanguage: (language) => set({ language }),
      reducedMotion: false,
      setReducedMotion: (reducedMotion) => set({ reducedMotion }),
      demoMode: true,
      setDemoMode: (demoMode) => set({ demoMode }),

      // Consent state
      consent: initialConsent,
      setConsent: (consentPartial) =>
        set((state) => ({ consent: { ...state.consent, ...consentPartial } })),
      completeConsent: () =>
        set((state) => ({
          consent: {
            ...state.consent,
            completedAt: new Date().toISOString(),
          },
        })),

      // Conversation state
      currentQuestionIndex: 0,
      answers: {},
      messages: [],
      interviewStatus: 'idle',
      setAnswer: (key, value) =>
        set((state) => ({
          answers: { ...state.answers, [key]: value },
        })),
      addMessage: (msg) =>
        set((state) => ({
          messages: [...state.messages, msg],
        })),
      confirmMessage: (id) =>
        set((state) => ({
          messages: state.messages.map((m) =>
            m.id === id ? { ...m, isConfirmed: true } : m
          ),
        })),
      editMessage: (id, newText) =>
        set((state) => ({
          messages: state.messages.map((m) =>
            m.id === id ? { ...m, text: newText, isConfirmed: true } : m
          ),
        })),
      nextQuestion: () =>
        set((state) => ({
          currentQuestionIndex: state.currentQuestionIndex + 1,
        })),
      prevQuestion: () =>
        set((state) => ({
          currentQuestionIndex: Math.max(0, state.currentQuestionIndex - 1),
        })),
      resetConversation: () =>
        set({
          currentQuestionIndex: 0,
          answers: {},
          messages: [],
          interviewStatus: 'idle',
        }),

      // Beneficiary state
      profile: null,
      userLocation: initialLocation,
      setProfile: (profile) => set({ profile }),
      setUserLocation: (userLocation) => set({ userLocation }),
      setEnrolledPathway: (pathwayId) =>
        set((state) => ({
          selectedPathwayId: pathwayId,
          profile: state.profile
            ? { ...state.profile, enrolledPathwayId: pathwayId, status: 'enrolled' }
            : null,
        })),

      // Recommendations state
      recommendations: [],
      selectedPathwayId: null,
      savedPathwayIds: [],
      setRecommendations: (recommendations) => set({ recommendations }),
      setSelectedPathwayId: (selectedPathwayId) => set({ selectedPathwayId }),
      toggleSavePathway: (id) =>
        set((state) => ({
          savedPathwayIds: state.savedPathwayIds.includes(id)
            ? state.savedPathwayIds.filter((item) => item !== id)
            : [...state.savedPathwayIds, id],
        })),

      // UI state
      sidebarOpen: false,
      setSidebarOpen: (sidebarOpen) => set({ sidebarOpen }),
      activeModal: null,
      setActiveModal: (activeModal) => set({ activeModal }),

      // Reset entire demo
      resetEntireDemo: () =>
        set({
          language: 'hi',
          consent: initialConsent,
          currentQuestionIndex: 0,
          answers: {},
          messages: [],
          interviewStatus: 'idle',
          profile: null,
          userLocation: initialLocation,
          recommendations: [],
          selectedPathwayId: null,
          savedPathwayIds: [],
        }),
    }),
    {
      name: 'jeevika-saarthi-storage',
      storage: createJSONStorage(() => localStorage),
    }
  )
);
