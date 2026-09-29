import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  User,
  Compass,
  CheckCircle2,
  Calendar,
  PhoneCall,
  MapPin,
  List,
  Map as MapIcon,
  Briefcase,
  AlertCircle,
  HelpCircle,
  ShieldCheck,
  Download,
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Progress } from '../components/ui/Progress';
import { EmptyState } from '../components/EmptyState';
import { MapPanel } from '../components/MapPanel';
import { DemoDataBadge } from '../components/DemoDataBadge';
import { PathwayTimeline } from '../components/PathwayTimeline';
import { useAppStore } from '../stores/useAppStore';
import { useRecommendations } from '../hooks/useRecommendations';
import { mockApi } from '../services/mockApi';
import { apiClient } from '../services/apiClient';
import { useQuery } from '@tanstack/react-query';
import { toast } from 'sonner';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { profile, selectedPathwayId, userLocation } = useAppStore();
  const { recommendations } = useRecommendations();
  const [oppViewMode, setOppViewMode] = useState<'list' | 'map'>('list');

  // Selected pathway or fallback
  const enrolledPathway =
    recommendations.find((p) => p.id === selectedPathwayId) || recommendations[0];

  const { data: opportunities = [] } = useQuery({
    queryKey: ['local-opportunities'],
    queryFn: () => mockApi.fetchLocalOpportunities(),
  });

  const handleAskFacilitatorHelp = () => {
    toast.success('Facilitator assistance request dispatched! Amit Singh (VLE Sadar) will contact you shortly.');
  };

  const beneficiaryName = profile?.name || 'Rajesh Kumar';

  return (
    <div className="max-w-7xl mx-auto py-6 px-4 space-y-8">
      {/* HEADER GREETING */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-white border border-slate-200 shadow-sm">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-extrabold text-slate-900">
              Welcome back, {beneficiaryName}!
            </h1>
            <Badge variant="success" className="text-xs">
              Profile Active
            </Badge>
            <DemoDataBadge text="Beneficiary Portal" />
          </div>
          <p className="text-xs text-slate-500">
            {profile?.location.village || 'Rampur Demo'}, {profile?.location.block || 'Sadar'}, {profile?.location.district || 'Lucknow'}
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handleAskFacilitatorHelp}
            className="gap-2 text-xs"
          >
            <HelpCircle className="h-4 w-4 text-brand-600" />
            <span>Ask Facilitator Help</span>
          </Button>
          <Link to="/conversation">
            <Button variant="secondary" size="sm" className="text-xs">
              Retake Voice Interview
            </Button>
          </Link>
        </div>
      </div>

      {/* DISCLAIMER BANNER */}
      <div className="p-3.5 rounded-xl bg-slate-900 text-white text-xs flex items-center justify-between gap-4 shadow-sm">
        <div className="flex items-center gap-2">
          <AlertCircle className="h-4 w-4 text-saffron-400 shrink-0" />
          <span>
            <strong>Demo Disclaimer:</strong> No job or financial grant is guaranteed. Local verification by a PM-AJAY facilitator is required.
          </span>
        </div>
        <DemoDataBadge text="Localhost seeded" className="py-0 px-2 text-[10px] hidden sm:inline-flex" />
      </div>

      {/* SELECTED PATHWAY SUMMARY OR EMPTY STATE */}
      {selectedPathwayId ? (
        <Card className="bg-gradient-to-r from-brand-900 via-slate-900 to-slate-900 text-white p-6 rounded-3xl shadow-xl">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Badge variant="saffron" className="text-xs">
                  Active Selected Pathway
                </Badge>
                <span className="text-xs text-brand-300 font-semibold">
                  NSQF Level {enrolledPathway.nsqfLevel}
                </span>
              </div>
              <h2 className="text-2xl font-extrabold text-white">{enrolledPathway.title}</h2>
              <p className="text-xs text-slate-300 max-w-xl">{enrolledPathway.fitReason}</p>
            </div>

            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 shrink-0">
              <Link to={`/pathway/${enrolledPathway.id}`}>
                <Button variant="accent" size="default" className="font-bold text-slate-900 gap-2">
                  <span>View Timeline & Centre</span>
                </Button>
              </Link>
            </div>
          </div>
        </Card>
      ) : (
        <EmptyState
          title="No Livelihood Pathway Selected Yet"
          description="Complete your voice interview or review your recommended pathways to select your primary skilling goal."
          actionText="Browse Recommended Pathways"
          onAction={() => navigate('/recommendations')}
        />
      )}

      {/* DASHBOARD GRID: STATUS & TIMELINE */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column */}
        <div className="lg:col-span-7 space-y-6">
          {/* Profile Completeness & Actions */}
          <Card className="bg-white border-slate-200 p-6 space-y-4">
            <div className="flex items-center justify-between text-xs">
              <span className="font-bold text-slate-900">Profile Completeness</span>
              <span className="font-extrabold text-brand-700">90% Complete</span>
            </div>
            <Progress value={90} indicatorColor="bg-brand-600" />
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 text-xs">
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-100 flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
                <span>Voice Interview Completed</span>
              </div>
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-100 flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
                <span>Extracted Profile Confirmed</span>
              </div>
            </div>
          </Card>

          {/* Timeline Progress */}
          {enrolledPathway && (
            <Card className="bg-white border-slate-200 p-6">
              <CardHeader className="p-0 mb-4">
                <CardTitle className="text-base font-bold text-slate-900">
                  Enrolled Pathway Milestones
                </CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                <PathwayTimeline milestones={enrolledPathway.milestones} currentStepIndex={0} />
              </CardContent>
            </Card>
          )}
        </div>

        {/* Right Column: Upcoming Follow-up & Facilitator */}
        <div className="lg:col-span-5 space-y-6">
          {/* Upcoming Follow-up Card */}
          <Card className="bg-white border-slate-200 p-6 space-y-4">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-saffron-100 text-saffron-800">
                <Calendar className="h-5 w-5" />
              </div>
              <div>
                <h3 className="font-bold text-slate-900 text-sm">Upcoming Verification Follow-up</h3>
                <span className="text-xs text-slate-400">Scheduled VLE Field Visit</span>
              </div>
            </div>
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-100 text-xs space-y-1">
              <div className="flex justify-between font-semibold">
                <span className="text-slate-500">Date:</span>
                <span className="text-slate-900">Tomorrow, 10:30 AM</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Facilitator:</span>
                <span className="text-brand-700 font-bold">Amit Singh (Sadar VLE)</span>
              </div>
            </div>
          </Card>

          {/* Facilitator Support Card */}
          <Card className="bg-white border-slate-200 p-6 space-y-4">
            <h3 className="font-bold text-slate-900 text-sm">Assigned PM-AJAY Facilitator</h3>
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-full bg-brand-700 text-white font-bold flex items-center justify-center text-sm">
                AS
              </div>
              <div>
                <div className="font-bold text-slate-900 text-sm">Amit Singh</div>
                <div className="text-xs text-slate-500">Block Facilitator, Sadar Lucknow</div>
              </div>
            </div>
            <Button
              variant="default"
              size="sm"
              onClick={handleAskFacilitatorHelp}
              className="w-full gap-2 text-xs"
            >
              <PhoneCall className="h-3.5 w-3.5" />
              <span>Call / Request Callback</span>
            </Button>
          </Card>

          {/* DPDP Consent & Privacy Hub */}
          <Card className="bg-slate-50 border-slate-200 p-5 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
                <ShieldCheck className="h-4 w-4 text-brand-600" />
                DPDP Privacy & Data Controls
              </span>
              <Badge variant="success" className="text-[10px]">Consent Active</Badge>
            </div>
            <p className="text-xs text-slate-500">
              You have full rights under Digital Personal Data Protection Act 2023. Download your data or manage consent anytime.
            </p>
            <div className="flex flex-col gap-2 pt-1">
              <Button
                variant="outline"
                size="sm"
                onClick={async () => {
                  try {
                    const data = await apiClient.exportPrivacyData();
                    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `jeevika_beneficiary_data_export_${new Date().toISOString().split('T')[0]}.json`;
                    a.click();
                    toast.success('Machine-readable DPDP data export downloaded successfully.');
                  } catch {
                    toast.error('Failed to export data. Please try again.');
                  }
                }}
                className="w-full gap-2 text-xs"
              >
                <Download className="h-3.5 w-3.5" />
                <span>Download My Data (JSON)</span>
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => {
                  toast.info('Consent settings: Profile, Recommendations & Retention tracking are currently active.');
                }}
                className="w-full text-xs text-slate-600"
              >
                <span>Manage Consent Preferences</span>
              </Button>
            </div>
          </Card>
        </div>
      </div>

      {/* LOCAL OPPORTUNITIES SECTION (WITH LIST / MAP TOGGLE) */}
      <section className="space-y-4 pt-4 border-t border-slate-200">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-slate-900">Local Livelihood Opportunities</h2>
            <p className="text-xs text-slate-500">
              Verified employer listings matching {profile?.location.block || 'Sadar'} block and surrounding clusters.
            </p>
          </div>

          <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200 self-start sm:self-auto">
            <button
              onClick={() => setOppViewMode('list')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                oppViewMode === 'list'
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              <List className="h-3.5 w-3.5" />
              <span>List View</span>
            </button>
            <button
              onClick={() => setOppViewMode('map')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                oppViewMode === 'map'
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              <MapIcon className="h-3.5 w-3.5" />
              <span>Map View</span>
            </button>
          </div>
        </div>

        {oppViewMode === 'list' ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {opportunities.map((opp) => (
              <Card key={opp.id} hoverEffect className="bg-white border-slate-200 p-5 space-y-3">
                <div className="flex items-center justify-between text-xs">
                  <Badge variant="default">{opp.type}</Badge>
                  <DemoDataBadge text="Verified Signal" className="py-0 px-1.5 text-[9px]" />
                </div>
                <h3 className="font-bold text-slate-900 text-sm leading-snug">{opp.title}</h3>
                <p className="text-xs text-slate-500">{opp.provider}</p>
                <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs">
                  <span className="text-emerald-700 font-bold">{opp.stipendSalary}</span>
                  <span className="text-slate-400">{opp.distanceKm} km away</span>
                </div>
              </Card>
            ))}
          </div>
        ) : (
          <MapPanel userLocation={userLocation} height="360px" />
        )}
      </section>
    </div>
  );
};
