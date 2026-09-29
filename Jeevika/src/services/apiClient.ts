/**
 * Jeevika Saarthi AI - Production API Client
 * Connects web frontend to FastAPI backend (/api/v1) with JWT auth, token rotation,
 * and seamless fallback handling.
 */

const BASE_URL = ((import.meta as any).env?.VITE_API_BASE_URL as string) || '/api/v1';

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  role: 'beneficiary' | 'facilitator' | 'admin';
}

export interface UserSession {
  id: string;
  email: string;
  fullName: string | null;
  role: 'beneficiary' | 'facilitator' | 'admin';
  isActive: boolean;
}

class ApiClient {
  private accessToken: string | null = null;
  private refreshToken: string | null = null;
  private userRole: string | null = null;

  constructor() {
    this.accessToken = localStorage.getItem('jeevika_access_token');
    this.refreshToken = localStorage.getItem('jeevika_refresh_token');
    this.userRole = localStorage.getItem('jeevika_user_role');
  }

  setSession(access: string, refresh: string, role: string) {
    this.accessToken = access;
    this.refreshToken = refresh;
    this.userRole = role;
    localStorage.setItem('jeevika_access_token', access);
    localStorage.setItem('jeevika_refresh_token', refresh);
    localStorage.setItem('jeevika_user_role', role);
  }

  clearSession() {
    this.accessToken = null;
    this.refreshToken = null;
    this.userRole = null;
    localStorage.removeItem('jeevika_access_token');
    localStorage.removeItem('jeevika_refresh_token');
    localStorage.removeItem('jeevika_user_role');
  }

  isAuthenticated(): boolean {
    return !!this.accessToken;
  }

  getRole(): string {
    return this.userRole || 'beneficiary';
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${BASE_URL}${endpoint}`;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string> || {}),
    };

    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    let res: Response;
    try {
      res = await fetch(url, { ...options, headers });
    } catch (networkError) {
      console.warn(`[ApiClient] Network request failed to ${endpoint}:`, networkError);
      throw networkError;
    }

    // Auto-refresh token on 401 if refresh token is available
    if (res.status === 401 && this.refreshToken && !endpoint.includes('/auth/refresh')) {
      const refreshed = await this.tryRefreshToken();
      if (refreshed) {
        headers['Authorization'] = `Bearer ${this.accessToken}`;
        res = await fetch(url, { ...options, headers });
      }
    }

    if (!res.ok) {
      let errorDetail = `HTTP ${res.status} ${res.statusText}`;
      try {
        const errorJson = await res.json();
        errorDetail = errorJson.detail || errorDetail;
      } catch {
        // ignore json parse error
      }
      throw new Error(errorDetail);
    }

    return res.json() as Promise<T>;
  }

  private async tryRefreshToken(): Promise<boolean> {
    if (!this.refreshToken) return false;
    try {
      const res = await fetch(`${BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: this.refreshToken }),
      });
      if (res.ok) {
        const data = await res.json();
        this.accessToken = data.access_token;
        localStorage.setItem('jeevika_access_token', data.access_token);
        return true;
      }
    } catch {
      this.clearSession();
    }
    return false;
  }

  // ================= Auth =================
  async login(email: string, password: string): Promise<AuthTokens> {
    const data = await this.request<{ access_token: string; refresh_token: string; role: any }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    this.setSession(data.access_token, data.refresh_token, data.role);
    return {
      accessToken: data.access_token,
      refreshToken: data.refresh_token,
      role: data.role,
    };
  }

  async register(payload: { email: string; password: string; full_name?: string; role?: string }): Promise<any> {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  async getCurrentUser(): Promise<UserSession> {
    return this.request<UserSession>('/auth/me');
  }

  async logout(): Promise<void> {
    try {
      if (this.accessToken) {
        await this.request('/auth/logout', { method: 'POST' });
      }
    } finally {
      this.clearSession();
    }
  }

  // ================= Beneficiaries =================
  async listBeneficiaries(params?: { district?: string; status?: string; search?: string }): Promise<any[]> {
    const query = new URLSearchParams();
    if (params?.district) query.set('district', params.district);
    if (params?.status) query.set('status_filter', params.status);
    if (params?.search) query.set('search', params.search);
    return this.request(`/beneficiaries?${query.toString()}`);
  }

  async getBeneficiary(id: string): Promise<any> {
    return this.request(`/beneficiaries/${id}`);
  }

  async createBeneficiary(payload: any): Promise<any> {
    return this.request('/beneficiaries', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  async updateBeneficiary(id: string, payload: any): Promise<any> {
    return this.request(`/beneficiaries/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    });
  }

  async recordLocationConsent(id: string, consentGranted: boolean): Promise<any> {
    return this.request(`/beneficiaries/${id}/location-consent`, {
      method: 'POST',
      body: JSON.stringify({ consent_granted: consentGranted }),
    });
  }

  async updateLocation(id: string, lat: number, lon: number, accuracyMeters?: number): Promise<any> {
    return this.request(`/beneficiaries/${id}/location`, {
      method: 'PUT',
      body: JSON.stringify({ latitude: lat, longitude: lon, accuracy_meters: accuracyMeters }),
    });
  }

  // ================= Voice Sessions & Profile Extraction =================
  async startVoiceSession(beneficiaryId: string, language: string = 'hi'): Promise<any> {
    return this.request('/sessions/start', {
      method: 'POST',
      body: JSON.stringify({ beneficiary_id: beneficiaryId, language }),
    });
  }

  async addSessionTurn(sessionId: string, speaker: 'assistant' | 'user', transcript: string, confidence: number = 0.95): Promise<any> {
    return this.request(`/sessions/${sessionId}/turn`, {
      method: 'POST',
      body: JSON.stringify({ speaker, transcript, confidence_score: confidence }),
    });
  }

  async extractProfile(sessionId: string, fullTranscript?: string): Promise<any> {
    return this.request(`/sessions/${sessionId}/extract-profile`, {
      method: 'POST',
      body: JSON.stringify({ full_transcript: fullTranscript }),
    });
  }

  async clarifyField(sessionId: string, fieldKey: string, clarificationResponse: string): Promise<any> {
    return this.request(`/sessions/${sessionId}/clarify`, {
      method: 'POST',
      body: JSON.stringify({ field_key: fieldKey, clarification_response: clarificationResponse }),
    });
  }

  async confirmProfile(sessionId: string, confirmedFields: Record<string, any>): Promise<any> {
    return this.request(`/sessions/${sessionId}/confirm-profile`, {
      method: 'POST',
      body: JSON.stringify({ confirmed_fields: confirmedFields }),
    });
  }

  async getFieldProvenance(sessionId: string): Promise<any> {
    return this.request(`/sessions/${sessionId}/field-provenance`);
  }

  // ================= Recommendations v2 =================
  async generateRecommendations(beneficiaryId: string, forceRefresh: boolean = false): Promise<any[]> {
    return this.request('/recommendations/generate', {
      method: 'POST',
      body: JSON.stringify({ beneficiary_id: beneficiaryId, force_refresh: forceRefresh }),
    });
  }

  async getBeneficiaryRecommendations(beneficiaryId: string): Promise<any[]> {
    return this.request(`/recommendations/beneficiary/${beneficiaryId}`);
  }

  async selectRecommendationPathway(beneficiaryId: string, pathwayId: string): Promise<any> {
    return this.request('/recommendations/select', {
      method: 'POST',
      body: JSON.stringify({ beneficiary_id: beneficiaryId, pathway_id: pathwayId }),
    });
  }

  // ================= Training Centres & Opportunities =================
  async getNearbyTrainingCentres(lat: number = 26.8467, lon: number = 80.9462, radiusKm: number = 50): Promise<any[]> {
    return this.request(`/training-centres/nearby?latitude=${lat}&longitude=${lon}&radius_km=${radiusKm}`);
  }

  async getNearbyOpportunities(district: string = 'Lucknow', sector?: string): Promise<any[]> {
    const query = new URLSearchParams({ district });
    if (sector) query.set('sector', sector);
    return this.request(`/opportunities/nearby?${query.toString()}`);
  }

  async getOpportunitySignals(district?: string, sector?: string): Promise<any[]> {
    const query = new URLSearchParams();
    if (district) query.set('district', district);
    if (sector) query.set('sector', sector);
    return this.request(`/opportunities/signals?${query.toString()}`);
  }

  // ================= Workflow & Human-in-the-Loop =================
  async getReviewTasks(status?: string, priority?: string): Promise<any[]> {
    const query = new URLSearchParams();
    if (status) query.set('status_filter', status);
    if (priority) query.set('priority_filter', priority);
    return this.request(`/reviews/tasks?${query.toString()}`);
  }

  async createReviewTask(payload: { beneficiary_id: string; task_type: string; priority: string; trigger_reason: string }): Promise<any> {
    return this.request('/reviews/tasks', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  async submitReviewTaskDecision(taskId: string, decision: string, decisionNotes?: string): Promise<any> {
    return this.request(`/reviews/tasks/${taskId}/decision`, {
      method: 'PUT',
      body: JSON.stringify({ decision, decision_notes: decisionNotes }),
    });
  }

  async createReferral(payload: {
    beneficiary_id: string;
    target_type: string;
    target_id: string;
    pathway_id?: string;
    counseling_summary?: string;
    idempotency_key?: string;
  }): Promise<any> {
    return this.request('/referrals', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  async getReferrals(beneficiaryId?: string): Promise<any[]> {
    const query = new URLSearchParams();
    if (beneficiaryId) query.set('beneficiary_id', beneficiaryId);
    return this.request(`/referrals?${query.toString()}`);
  }

  async updateReferralProgress(referralId: string, status: string, providerFeedback?: string): Promise<any> {
    return this.request(`/referrals/${referralId}/progress`, {
      method: 'PUT',
      body: JSON.stringify({ status, provider_feedback: providerFeedback }),
    });
  }

  async getCaseTimeline(beneficiaryId: string): Promise<any[]> {
    return this.request(`/cases/${beneficiaryId}/timeline`);
  }

  // ================= Outcomes & Follow-ups =================
  async logTrainingProgress(payload: {
    beneficiary_id: string;
    training_centre_id: string;
    qp_code: string;
    attendance_percentage: number;
    modules_completed?: number;
    assessment_status: string;
    certification_number?: string;
  }): Promise<any> {
    return this.request('/outcomes/training-progress', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  async logEmploymentOutcome(payload: {
    beneficiary_id: string;
    employer_name: string;
    role_title: string;
    joining_date: string;
    monthly_wage_inr?: number;
    verification_method?: string;
  }): Promise<any> {
    return this.request('/outcomes/employment', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  async logEnterpriseOutcome(payload: {
    beneficiary_id: string;
    enterprise_name: string;
    activity_type: string;
    udyam_or_shg_id?: string;
    credit_scheme_linked?: string;
    loan_amount_sanctioned_inr?: number;
    monthly_estimated_revenue_inr?: number;
  }): Promise<any> {
    return this.request('/outcomes/enterprise', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  async getFollowUps(beneficiaryId?: string, milestone?: string): Promise<any[]> {
    const query = new URLSearchParams();
    if (beneficiaryId) query.set('beneficiary_id', beneficiaryId);
    if (milestone) query.set('milestone', milestone);
    return this.request(`/outcomes/follow-ups?${query.toString()}`);
  }

  async completeFollowUp(id: string, outcomeSummary: string, isRetained: boolean = true): Promise<any> {
    return this.request(`/outcomes/follow-ups/${id}/complete`, {
      method: 'PUT',
      body: JSON.stringify({ status: 'completed', outcome_summary: outcomeSummary, is_retained: isRetained }),
    });
  }

  // ================= Consent & DPDP Privacy =================
  async getConsents(): Promise<any[]> {
    return this.request('/consents');
  }

  async grantConsent(purpose: string, consentText: string, language: string = 'hi'): Promise<any> {
    return this.request('/consents', {
      method: 'POST',
      body: JSON.stringify({ purpose, consent_text: consentText, language }),
    });
  }

  async withdrawConsent(purpose: string): Promise<any> {
    return this.request(`/consents/${purpose}/withdraw`, { method: 'POST' });
  }

  async exportPrivacyData(): Promise<any> {
    return this.request('/privacy/export');
  }

  async requestDataDeletion(reason?: string): Promise<any> {
    const query = new URLSearchParams();
    if (reason) query.set('reason', reason);
    return this.request(`/privacy/request-deletion?${query.toString()}`, { method: 'DELETE' });
  }

  // ================= Admin Diagnostics & Imports =================
  async getAdminMetrics(district?: string): Promise<any> {
    const query = new URLSearchParams();
    if (district) query.set('district', district);
    return this.request(`/admin/metrics?${query.toString()}`);
  }

  async getDataQuality(): Promise<any> {
    return this.request('/admin/data-quality');
  }

  async getAuditEvents(limit: number = 50): Promise<any[]> {
    return this.request(`/admin/audit-events?limit=${limit}`);
  }

  async validateImport(batchType: string, sourceId: string, items: any[]): Promise<any> {
    return this.request('/admin/imports/validate', {
      method: 'POST',
      body: JSON.stringify({ batch_type: batchType, source_id: sourceId, items }),
    });
  }

  async publishImport(batchId: string): Promise<any> {
    return this.request(`/admin/imports/${batchId}/publish`, { method: 'POST' });
  }

  async rollbackImport(batchId: string): Promise<any> {
    return this.request(`/admin/imports/${batchId}/rollback`, { method: 'POST' });
  }

  // ================= Bhashini Voice AI =================
  async transcribeBhashini(audioBase64: string, language: string = 'hi'): Promise<{ success: boolean; transcript: string; provider: string }> {
    return this.request('/bhashini/asr', {
      method: 'POST',
      body: JSON.stringify({ audio_base64: audioBase64, language, audio_format: 'wav' }),
    });
  }

  async synthesizeBhashini(text: string, language: string = 'hi', gender: string = 'female'): Promise<{ success: boolean; audio_base64: string | null; provider: string }> {
    return this.request('/bhashini/tts', {
      method: 'POST',
      body: JSON.stringify({ text, language, gender }),
    });
  }
}

export const apiClient = new ApiClient();
