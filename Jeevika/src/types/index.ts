export type SupportedLanguage = 
  | 'hi' // Hindi
  | 'en' // English
  | 'mr' // Marathi
  | 'bn' // Bengali
  | 'ta' // Tamil
  | 'te' // Telugu
  | 'or' // Odia
  | 'gu' // Gujarati
  | 'kn' // Kannada
  | 'ml'; // Malayalam

export interface LanguageOption {
  code: SupportedLanguage;
  nameNative: string;
  nameEnglish: string;
  region: string;
}

export interface ConsentState {
  profileCreation: boolean;
  recommendations: boolean;
  followUp: boolean;
  completedAt: string | null;
}

export interface GeoLocation {
  state: string;
  district: string;
  block: string;
  village: string;
  pincode?: string;
  latitude: number;
  longitude: number;
  dataStatus: 'demo_seeded' | 'user_geolocated';
}

export interface InterviewQuestion {
  id: number;
  key: string;
  promptHi: string;
  promptEn: string;
  audioSampleHi?: string;
  quickChipsHi: string[];
  quickChipsEn: string[];
}

export interface ChatMessage {
  id: string;
  sender: 'assistant' | 'user';
  text: string;
  timestamp: string;
  audioUrl?: string;
  isConfirmed?: boolean;
}

export interface BeneficiaryProfile {
  id: string;
  name: string;
  phone: string;
  language: SupportedLanguage;
  gender: string;
  age: number;
  category: string;
  location: GeoLocation;
  education: string;
  currentWork: string;
  workExperienceYears: number;
  skills: string[];
  aspirations: string;
  preferences: {
    employmentType: 'wage_employment' | 'self_employment' | 'either';
    maxTravelKm: number;
    migration: boolean;
    hasVehicle: boolean;
    preferredSector?: string;
  };
  extractedProfile: {
    educationLevel: string;
    primarySkillSet: string;
    yearsExperience: string;
    mobilityPreference: string;
    preferredOutcome: string;
    confidenceScore: number;
    dataStatus: 'demo_seeded';
  };
  enrolledPathwayId: string | null;
  status: 'draft' | 'interview_completed' | 'profile_confirmed' | 'enrolled';
}

export interface TrainingCentre {
  id: string;
  name: string;
  address: string;
  district: string;
  state: string;
  latitude: number;
  longitude: number;
  distanceKm: number;
  contactPerson: string;
  phone: string;
  accreditedSectors: string[];
  facilities: string[];
  rating: number;
  dataStatus: 'demo_seeded';
}

export interface Milestone {
  title: string;
  description: string;
  duration: string;
  status: 'completed' | 'in_progress' | 'pending';
}

export interface PathwayRecommendation {
  id: string;
  rank: number;
  qpCode: string;
  title: string;
  nsqfLevel: number;
  sector: string;
  suitabilityScore: number;
  fitReason: string;
  matchReasons: string[];
  skillGaps: string[];
  bridgeModules: string[];
  nearestCentre: {
    id: string;
    name: string;
    distanceKm: number;
    estimatedTravelTimeMinutes: number;
  };
  durationWeeks: number;
  localDemandSignal: string;
  rplEligible: boolean;
  estimatedEarnings: string;
  riskWarning: string;
  nextSteps: string[];
  milestones: Milestone[];
  dataStatus: 'demo_seeded';
}

export interface LocalOpportunity {
  id: string;
  title: string;
  provider: string;
  type: string;
  location: string;
  distanceKm: number;
  stipendSalary: string;
  qualificationRequired: string;
  openings: number;
  latitude: number;
  longitude: number;
  postedDate: string;
  dataStatus: 'demo_seeded';
}

export interface FacilitatorCase {
  id: string;
  beneficiaryId: string;
  beneficiaryName: string;
  phone: string;
  block: string;
  village: string;
  recommendedPathway: string;
  assignedFacilitator: string;
  verificationStatus: 'pending_document_check' | 'verified' | 'enrolled' | 'action_required';
  documentChecklist: {
    aadhaarConsent: boolean;
    class10Certificate: boolean;
    bankDetails: boolean;
    casteDeclaration: boolean;
  };
  lastInteractionDate: string;
  nextFollowUpDate: string;
  riskFlag: string;
  notes: string;
  dataStatus: 'demo_seeded';
}

export interface AdminAnalytics {
  district: string;
  state: string;
  lastUpdated: string;
  kpis: {
    totalBeneficiariesProfiled: number;
    recommendationAcceptanceRate: number;
    activeEnrolments: number;
    placementEnterpriseOutcomes: number;
    dataStatus: 'demo_seeded';
  };
  monthlyTrend: Array<{ month: string; profiled: number; enrolled: number; outcomes: number }>;
  sectorBreakdown: Array<{ sector: string; value: number; percentage: number }>;
  blockLivelihoodSignals: Array<{
    block: string;
    profiled: number;
    topSector: string;
    trainingCentreCount: number;
    demandLevel: string;
  }>;
  trainingProviders: Array<{
    name: string;
    capacity: number;
    activeBatch: number;
    placementRate: number;
    status: string;
  }>;
  dataStatus: 'demo_seeded';
}
