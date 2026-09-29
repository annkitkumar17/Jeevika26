import {
  BeneficiaryProfile,
  PathwayRecommendation,
  TrainingCentre,
  LocalOpportunity,
  FacilitatorCase,
  AdminAnalytics,
} from '../types';
import { apiClient } from './apiClient';

export interface QualificationOption {
  qpCode: string;
  title: string;
  nsqfLevel: number;
  sector: string;
  description: string;
  prerequisites: string;
  durationHours: number;
  rplEligible: boolean;
  avgSalaryRange: string;
  selfEmploymentPotential: string;
  dataStatus: 'verified' | 'demo_seeded';
}

export const mockApi = {
  // 1. Fetch beneficiary profile from backend / local storage fallback
  async fetchBeneficiaryProfile(): Promise<BeneficiaryProfile> {
    try {
      const beneficiaries = await apiClient.listBeneficiaries();
      if (beneficiaries && beneficiaries.length > 0) {
        const ben = beneficiaries[0];
        return {
          id: ben.id,
          name: ben.name,
          phone: ben.phone || '+91 98765 12345',
          language: ben.preferred_language || 'hi',
          gender: ben.gender || 'male',
          age: ben.age || 28,
          category: 'SC / PM-AJAY Eligible',
          location: {
            state: ben.state || 'Uttar Pradesh',
            district: ben.district || 'Lucknow',
            block: ben.block || 'Sadar',
            village: ben.village || 'Rampur Demo',
            latitude: ben.latitude || 26.8467,
            longitude: ben.longitude || 80.9462,
            dataStatus: ben.location_consent_granted ? 'user_geolocated' : 'demo_seeded',
          },
          education: ben.education || 'Class 10 Pass',
          currentWork: ben.current_work || 'Agri Pump Mechanic Assistant',
          workExperienceYears: parseInt(ben.experience_years) || 3,
          skills: ben.skills || ['Mechanical Repair', 'Tool Handling', 'Customer Support'],
          aspirations: ben.traditional_occupation || 'Solar pump installation & maintenance',
          preferences: {
            employmentType: ben.preferences?.employment_type || 'self_employment',
            maxTravelKm: ben.preferences?.max_travel_km || 25,
            migration: ben.preferences?.migration || false,
            hasVehicle: true,
            preferredSector: 'Green Jobs / Renewable Energy',
          },
          extractedProfile: {
            educationLevel: ben.education || 'Class 10',
            primarySkillSet: (ben.skills && ben.skills.join(', ')) || 'Mechanical Repair',
            yearsExperience: ben.experience_years || '3 years',
            mobilityPreference: `Within ${ben.preferences?.max_travel_km || 25} km`,
            preferredOutcome: ben.preferences?.employment_type || 'Self-employment',
            confidenceScore: ben.field_provenance?.confidence_score || 94,
            dataStatus: 'demo_seeded',
          },
          enrolledPathwayId: ben.enrolled_pathway_id || null,
          status: ben.status as any || 'profiled',
        };
      }
    } catch (err) {
      console.warn('[mockApi] Falling back to local template profile:', err);
    }

    const res = await fetch('/mock-data/beneficiary.json');
    return res.json();
  },

  // 2. Update beneficiary profile
  async updateBeneficiaryProfile(profile: Partial<BeneficiaryProfile>): Promise<BeneficiaryProfile> {
    try {
      if (profile.id) {
        await apiClient.updateBeneficiary(profile.id, {
          name: profile.name,
          education: profile.education,
          current_work: profile.currentWork,
          experience_years: `${profile.workExperienceYears || 3} years`,
          skills: profile.skills,
          preferences: profile.preferences,
        });
      }
    } catch (err) {
      console.warn('[mockApi] Backend update failed, updating locally:', err);
    }
    const current = await this.fetchBeneficiaryProfile();
    return { ...current, ...profile };
  },

  // 3. Generate Profile from interactive interview answers
  async generateProfileFromInterview(answers: Record<string, string>): Promise<BeneficiaryProfile> {
    const base = await this.fetchBeneficiaryProfile();
    const currentWork = answers['currentWork'] || base.currentWork;
    const education = answers['education'] || base.education;
    const aspirations = answers['interestArea'] || answers['aspirations'] || base.aspirations;
    const empType = (answers['employmentType']?.toLowerCase().includes('wage') ? 'wage_employment' : 'self_employment') as any;
    const skills = answers['skills'] ? answers['skills'].split(',').map(s => s.trim()) : base.skills;

    try {
      // 1. Create session and extract profile on backend
      const sessionRes = await apiClient.startVoiceSession(base.id, base.language);
      if (sessionRes?.id) {
        const transcriptSummary = Object.entries(answers).map(([k, v]) => `${k}: ${v}`).join('. ');
        await apiClient.extractProfile(sessionRes.id, transcriptSummary);
        await apiClient.confirmProfile(sessionRes.id, {
          education,
          current_work: currentWork,
          skills,
          aspirations,
        });
      }
    } catch (err) {
      console.warn('[mockApi] Voice extraction session created locally:', err);
    }

    return {
      ...base,
      currentWork,
      education,
      aspirations,
      skills,
      preferences: {
        ...base.preferences,
        employmentType: empType,
      },
      extractedProfile: {
        ...base.extractedProfile,
        educationLevel: education,
        primarySkillSet: currentWork,
        preferredOutcome: answers['employmentType'] || 'Self-employment',
        confidenceScore: 96,
      },
      status: 'interview_completed',
    };
  },

  // 4. Recommendations Engine v2
  async generateRecommendations(profile: BeneficiaryProfile): Promise<PathwayRecommendation[]> {
    try {
      const backendRecs = await apiClient.generateRecommendations(profile.id, true);
      if (backendRecs && backendRecs.length > 0) {
        return backendRecs.map((rec: any, idx: number) => ({
          id: rec.id || `pathway-v2-${idx + 1}`,
          rank: rec.rank || (idx + 1),
          qpCode: rec.qp_code,
          title: rec.title,
          nsqfLevel: rec.nsqf_level,
          sector: rec.sector,
          suitabilityScore: Math.round((rec.overall_score || 0.85) * 100),
          fitReason: rec.fit_reason || 'Strong alignment with prior mechanical skills and PM-KUSUM expansion.',
          matchReasons: rec.why_this_fits || [
            'Direct alignment with 3 years pump maintenance experience',
            'Near-home PMKK training facility within 18 km',
            'RPL Fast-track eligible with 4 bridge modules',
          ],
          skillGaps: (rec.skill_gaps && rec.skill_gaps.map((g: any) => typeof g === 'string' ? g : g.nos_unit_title || g.gap_type)) || [
            'Micro-inverter grid synchronization and telemetry protocols',
            'Safe DC high-voltage cabling & earthing standards',
          ],
          bridgeModules: rec.bridge_modules || [
            'Safety & Earthing for Solar PV (15 hrs)',
            'DC Inverter Diagnostics & IoT Telemetry (25 hrs)',
          ],
          nearestCentre: {
            id: rec.nearest_centre_id || 'PMKK-SADAR-01',
            name: rec.nearest_centre_name || 'PMKK Lucknow Sadar Center',
            distanceKm: rec.distance_km || 18.4,
            estimatedTravelTimeMinutes: Math.round((rec.distance_km || 18.4) * 2.2),
          },
          durationWeeks: rec.duration_weeks || 6,
          localDemandSignal: rec.local_demand_signal || 'High (42 verified micro-grid installations under PM-KUSUM)',
          rplEligible: rec.rpl_eligible ?? true,
          estimatedEarnings: rec.estimated_earnings_range || '₹18,000 - ₹24,000 / month',
          riskWarning: rec.risks && rec.risks.length > 0 ? rec.risks[0] : 'Requires daily commute to Sadar centre.',
          nextSteps: rec.next_actions || [
            'Complete Facilitator physical verification',
            'Enroll at PMKK Sadar centre for 2-week bridge module',
            'Apply for PM-MUDRA tool kit credit support',
          ],
          milestones: [
            { title: 'RPL Assessment & Prior Recognition', description: 'Evaluate existing repair experience', duration: 'Week 1', status: 'pending' },
            { title: 'Bridge Skill Practical Training', description: 'Hands-on training at verified centre', duration: 'Weeks 2-5', status: 'pending' },
            { title: 'NSQF Certification & Placement Linkage', description: 'Formal assessment and industry referral', duration: 'Week 6', status: 'pending' },
          ],
          dataStatus: 'verified' as any,
        }));
      }
    } catch (err) {
      console.warn('[mockApi] Backend recommendations call failed, using fallback:', err);
    }

    const res = await fetch('/mock-data/recommendations.json');
    return res.json();
  },

  async fetchRecommendations(): Promise<PathwayRecommendation[]> {
    const profile = await this.fetchBeneficiaryProfile();
    return this.generateRecommendations(profile);
  },

  // 5. Training Centres
  async fetchTrainingCentres(): Promise<TrainingCentre[]> {
    try {
      const centres = await apiClient.getNearbyTrainingCentres(26.8467, 80.9462, 50);
      if (centres && centres.length > 0) {
        return centres.map((c: any) => ({
          id: c.id,
          name: c.name,
          address: c.address,
          district: c.district,
          state: c.state,
          latitude: c.latitude,
          longitude: c.longitude,
          distanceKm: c.distance_km || 12.5,
          contactPerson: c.contact_person || 'Centre Superintendent',
          phone: c.contact_phone || '+91 522 234 5678',
          accreditedSectors: c.accredited_sectors || ['Green Jobs', 'Agriculture'],
          facilities: c.facilities || ['Solar Lab', 'Hostel', 'Computer Lab', 'Smart Classroom'],
          rating: c.rating || 4.8,
          dataStatus: 'verified' as any,
        }));
      }
    } catch (err) {
      console.warn('[mockApi] Using fallback centres:', err);
    }

    const res = await fetch('/mock-data/training-centres.json');
    return res.json();
  },

  // 6. Local Opportunities
  async fetchLocalOpportunities(): Promise<LocalOpportunity[]> {
    try {
      const opps = await apiClient.getNearbyOpportunities('Lucknow');
      if (opps && opps.length > 0) {
        return opps.map((o: any) => ({
          id: o.id,
          title: o.title,
          provider: o.employer_name || 'Verified Employer',
          type: o.employment_type === 'wage_employment' ? 'Wage Employment' : 'Self-Employment / SHG',
          location: `${o.block || 'Sadar'}, ${o.district || 'Lucknow'}`,
          distanceKm: o.distance_km || 14,
          stipendSalary: o.wage_or_stipend || '₹16,000 - ₹22,000 / mo',
          qualificationRequired: 'Class 8 / 10 Pass',
          openings: o.openings || 10,
          latitude: 26.8467,
          longitude: 80.9462,
          postedDate: o.observed_date || '2026-09-15',
          dataStatus: 'demo_seeded',
        }));
      }
    } catch (err) {
      console.warn('[mockApi] Using fallback opportunities:', err);
    }

    const res = await fetch('/mock-data/local-opportunities.json');
    return res.json();
  },

  // 7. Facilitator Cases & Review Tasks
  async fetchFacilitatorCases(): Promise<FacilitatorCase[]> {
    try {
      const tasks = await apiClient.getReviewTasks();
      if (tasks && tasks.length > 0) {
        return tasks.map((t: any, idx: number) => ({
          id: t.id,
          beneficiaryId: t.beneficiary_id || `ben-0${idx + 1}`,
          beneficiaryName: `Candidate ${idx + 1} (${t.task_type})`,
          phone: '+91 98765 12345',
          village: 'Rampur / Sadar',
          block: 'Sadar',
          recommendedPathway: t.trigger_reason || 'Solar Pump Technician (NSQF Level 4)',
          assignedFacilitator: 'Amit Singh',
          verificationStatus: t.status === 'resolved' ? 'verified' : (t.status === 'in_review' ? 'pending_document_check' : 'pending_document_check'),
          documentChecklist: {
            aadhaarConsent: true,
            class10Certificate: true,
            bankDetails: true,
            casteDeclaration: true,
          },
          lastInteractionDate: t.created_at ? t.created_at.split('T')[0] : '2026-09-28',
          nextFollowUpDate: '2026-10-15',
          riskFlag: t.priority === 'high' ? 'Mobility / Prerequisite check required' : 'Normal',
          notes: t.decision_notes || t.trigger_reason,
          dataStatus: 'demo_seeded',
        }));
      }
    } catch (err) {
      console.warn('[mockApi] Using fallback facilitator cases:', err);
    }

    const res = await fetch('/mock-data/facilitator-cases.json');
    return res.json();
  },

  async updateCaseStatus(
    caseId: string,
    status: FacilitatorCase['verificationStatus'],
    notes?: string
  ): Promise<FacilitatorCase> {
    try {
      await apiClient.submitReviewTaskDecision(caseId, status === 'verified' ? 'approved' : 'rejected', notes);
    } catch (err) {
      console.warn('[mockApi] Updating case decision locally:', err);
    }
    const cases = await this.fetchFacilitatorCases();
    const item = cases.find((c) => c.id === caseId) || cases[0];
    return {
      ...item,
      verificationStatus: status,
      notes: notes || item.notes,
      lastInteractionDate: new Date().toISOString().split('T')[0],
    };
  },

  // 8. Admin Analytics & Diagnostics
  async fetchAdminAnalytics(): Promise<AdminAnalytics> {
    try {
      const metrics = await apiClient.getAdminMetrics('Lucknow');
      if (metrics) {
        return {
          district: 'Lucknow',
          state: 'Uttar Pradesh',
          lastUpdated: new Date().toISOString().split('T')[0],
          kpis: {
            totalBeneficiariesProfiled: metrics.total_beneficiaries || 1284,
            recommendationAcceptanceRate: metrics.acceptance_rate || 84.6,
            activeEnrolments: metrics.active_sessions || 742,
            placementEnterpriseOutcomes: metrics.retention_rate_30_days || 518,
            dataStatus: 'demo_seeded',
          },
          monthlyTrend: [
            { month: 'Apr', profiled: 120, enrolled: 80, outcomes: 45 },
            { month: 'May', profiled: 180, enrolled: 120, outcomes: 75 },
            { month: 'Jun', profiled: 240, enrolled: 160, outcomes: 110 },
            { month: 'Jul', profiled: 310, enrolled: 210, outcomes: 155 },
            { month: 'Aug', profiled: 390, enrolled: 280, outcomes: 210 },
            { month: 'Sep', profiled: 480, enrolled: 360, outcomes: 280 },
          ],
          sectorBreakdown: [
            { sector: 'Green Jobs / Solar', value: 432, percentage: 34.6 },
            { sector: 'Agriculture & Food Processing', value: 312, percentage: 25.0 },
            { sector: 'Handicrafts & Handlooms', value: 284, percentage: 22.8 },
            { sector: 'Healthcare / Nursing Aid', value: 220, percentage: 17.6 },
          ],
          blockLivelihoodSignals: [
            { block: 'Sadar', profiled: 412, topSector: 'Solar Microgrid', trainingCentreCount: 14, demandLevel: 'High' },
            { block: 'Mohanlalganj', profiled: 320, topSector: 'Food Processing', trainingCentreCount: 9, demandLevel: 'High' },
            { block: 'Malihabad', profiled: 280, topSector: 'Horticulture & Agro', trainingCentreCount: 7, demandLevel: 'Moderate' },
            { block: 'Bakshi Ka Talab', profiled: 272, topSector: 'Electrical Technician', trainingCentreCount: 6, demandLevel: 'Moderate' },
          ],
          trainingProviders: [
            { name: 'PMKK Sadar Tech Hub', capacity: 250, activeBatch: 180, placementRate: 88, status: 'Active' },
            { name: 'Jan Shikshan Sansthan Mohanlalganj', capacity: 180, activeBatch: 140, placementRate: 82, status: 'Active' },
            { name: 'Govt ITI Alambagh Center', capacity: 300, activeBatch: 220, placementRate: 85, status: 'Active' },
          ],
          dataStatus: 'demo_seeded',
        };
      }
    } catch (err) {
      console.warn('[mockApi] Using fallback analytics:', err);
    }

    const res = await fetch('/mock-data/admin-analytics.json');
    return res.json();
  },
};
