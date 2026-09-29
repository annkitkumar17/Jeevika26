import React, { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  ArrowLeft,
  CheckCircle2,
  MapPin,
  Clock,
  Sparkles,
  FileCheck,
  AlertTriangle,
  Award,
  Calendar,
  Share2,
  PhoneCall,
  Navigation,
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { PathwayTimeline } from '../components/PathwayTimeline';
import { MapPanel } from '../components/MapPanel';
import { DemoDataBadge } from '../components/DemoDataBadge';
import { ConfirmDialog } from '../components/ConfirmDialog';
import { useRecommendations } from '../hooks/useRecommendations';
import { useAppStore } from '../stores/useAppStore';
import { formatDistanceDemo, estimateTravelTimeMinutes } from '../lib/geo';
import { apiClient } from '../services/apiClient';

export const PathwayDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { recommendations } = useRecommendations();
  const { profile, userLocation, setEnrolledPathway } = useAppStore();

  const [showConfirmModal, setShowConfirmModal] = useState(false);

  const pathway = recommendations.find((p) => p.id === id) || recommendations[0];

  if (!pathway) {
    return (
      <div className="p-8 text-center space-y-4">
        <p className="text-sm text-slate-500">Pathway not found.</p>
        <Link to="/recommendations">
          <Button variant="default" size="sm">Back to Recommendations</Button>
        </Link>
      </div>
    );
  }

  const travelMinutes = estimateTravelTimeMinutes(pathway.nearestCentre.distanceKm);

  const documentChecklist = [
    { name: 'Class 10 Marksheet / Passing Certificate', status: 'ready' },
    { name: 'Aadhaar Card Consent Copy', status: 'ready' },
    { name: 'Bank Passbook / Jan Dhan Account', status: 'pending' },
    { name: 'Category Declaration (SC PM-AJAY beneficiary)', status: 'ready' },
  ];

  const handleConfirmEnrollment = async () => {
    setEnrolledPathway(pathway.id);
    if (profile?.id) {
      try {
        await apiClient.selectRecommendationPathway(profile.id, pathway.id);
      } catch (err) {
        console.warn('Backend pathway enrollment note:', err);
      }
    }
    navigate('/dashboard');
  };

  return (
    <div className="max-w-7xl mx-auto py-6 px-4 space-y-8">
      {/* BREADCRUMB */}
      <div className="flex items-center gap-2 text-xs font-semibold text-slate-500">
        <Link to="/recommendations" className="hover:text-brand-700 flex items-center gap-1">
          <ArrowLeft className="h-3.5 w-3.5" />
          <span>Pathways</span>
        </Link>
        <span>/</span>
        <span className="text-slate-900 font-bold">{pathway.title}</span>
      </div>

      {/* HEADER BANNER */}
      <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 text-white shadow-xl space-y-4 relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Badge variant="saffron" className="font-bold text-xs">
                Rank #{pathway.rank}
              </Badge>
              <Badge variant="default" className="text-xs">
                NSQF Level {pathway.nsqfLevel}
              </Badge>
              <DemoDataBadge text="Seeded QP Code: ELE/Q6301" className="py-0.5 px-2 text-[10px]" />
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white">{pathway.title}</h1>
            <p className="text-xs text-brand-300 font-semibold">{pathway.sector}</p>
          </div>

          <div className="flex items-center gap-3">
            <div className="text-right">
              <div className="text-2xl font-black text-emerald-400">{pathway.suitabilityScore}%</div>
              <div className="text-[10px] text-slate-400 uppercase font-semibold">Suitability Fit</div>
            </div>
            <Button
              variant="accent"
              size="lg"
              onClick={() => setShowConfirmModal(true)}
              className="gap-2 font-bold text-slate-900 shadow-lg"
            >
              <span>Enroll in Pathway</span>
            </Button>
          </div>
        </div>

        {/* Why this pathway fits */}
        <div className="p-4 rounded-2xl bg-slate-800/80 border border-slate-700 text-xs text-slate-200 leading-relaxed">
          <div className="font-bold text-saffron-400 mb-1 flex items-center gap-1.5">
            <Sparkles className="h-4 w-4 text-saffron-400" />
            <span>Why this pathway fits your profile:</span>
          </div>
          <p>{pathway.fitReason}</p>
        </div>
      </div>

      {/* MAIN CONTENT GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Timeline & Map */}
        <div className="lg:col-span-8 space-y-8">
          {/* Milestone Timeline */}
          <Card className="bg-white border-slate-200 p-6">
            <CardHeader className="p-0 mb-6">
              <CardTitle className="text-lg font-bold text-slate-900 flex items-center justify-between">
                <span>Pathway Milestone Timeline</span>
                <span className="text-xs text-slate-500 font-normal">Duration: {pathway.durationWeeks} Weeks</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <PathwayTimeline milestones={pathway.milestones} currentStepIndex={0} />
            </CardContent>
          </Card>

          {/* Training Centre & Map */}
          <Card className="bg-white border-slate-200 p-6">
            <CardHeader className="p-0 mb-4 flex flex-row items-center justify-between">
              <div>
                <CardTitle className="text-lg font-bold text-slate-900">Nearby Demo Training Centre</CardTitle>
                <p className="text-xs text-slate-500">Accredited PMKK Sadar hub within your mobility radius</p>
              </div>
              <Badge variant="default" className="text-xs">
                {formatDistanceDemo(pathway.nearestCentre.distanceKm)}
              </Badge>
            </CardHeader>
            <CardContent className="p-0 space-y-4">
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-100 flex flex-col sm:flex-row justify-between gap-4 text-xs">
                <div className="space-y-1">
                  <div className="font-bold text-slate-900 text-sm">{pathway.nearestCentre.name}</div>
                  <div className="text-slate-600 flex items-center gap-1">
                    <MapPin className="h-3.5 w-3.5 text-brand-600 shrink-0" />
                    <span>Sector 4, Industrial Area, Sadar, Lucknow</span>
                  </div>
                  <div className="text-slate-500 flex items-center gap-1">
                    <Clock className="h-3.5 w-3.5 text-slate-400 shrink-0" />
                    <span>Est. travel time: ~{travelMinutes} mins by bus / auto</span>
                  </div>
                </div>
                <div className="flex flex-col items-end justify-center shrink-0">
                  <Button variant="outline" size="sm" className="gap-1 text-xs">
                    <PhoneCall className="h-3.5 w-3.5" />
                    <span>Contact Centre</span>
                  </Button>
                </div>
              </div>

              {/* MapPanel */}
              <MapPanel userLocation={userLocation} height="280px" />
            </CardContent>
          </Card>

          {/* Document Readiness Checklist */}
          <Card className="bg-white border-slate-200 p-6">
            <CardHeader className="p-0 mb-4">
              <CardTitle className="text-lg font-bold text-slate-900">What You Need Next (Document Readiness)</CardTitle>
            </CardHeader>
            <CardContent className="p-0 space-y-3">
              {documentChecklist.map((doc, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 rounded-xl border border-slate-100 bg-slate-50 text-xs">
                  <div className="flex items-center gap-2.5">
                    <FileCheck className="h-4 w-4 text-brand-600" />
                    <span className="font-semibold text-slate-800">{doc.name}</span>
                  </div>
                  <Badge variant={doc.status === 'ready' ? 'success' : 'warning'} className="text-[10px]">
                    {doc.status === 'ready' ? 'Ready' : 'Pending Verification'}
                  </Badge>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Right Sidebar */}
        <div className="lg:col-span-4 space-y-6">
          {/* Enrolment Status Card */}
          <Card className="bg-white border-slate-200 p-6 space-y-4">
            <h3 className="text-base font-bold text-slate-900">Pathway Action Summary</h3>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-500">Status:</span>
                <span className="font-bold text-amber-600">Pending Selection</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-500">Est. Earnings:</span>
                <span className="font-bold text-emerald-700">{pathway.estimatedEarnings}</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-500">RPL Possibility:</span>
                <span className="font-bold text-slate-900">{pathway.rplEligible ? 'Yes (Fast-track)' : 'Full Training'}</span>
              </div>
            </div>

            <Button
              variant="default"
              size="lg"
              onClick={() => setShowConfirmModal(true)}
              className="w-full font-bold shadow-md"
            >
              Select & Enroll in Pathway
            </Button>
          </Card>

          {/* Risk & Safety */}
          {pathway.riskWarning && (
            <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-900 text-xs space-y-2">
              <div className="font-bold flex items-center gap-1.5">
                <AlertTriangle className="h-4 w-4 text-amber-600" />
                <span>Risk & Safety Advisory:</span>
              </div>
              <p className="leading-relaxed">{pathway.riskWarning}</p>
            </div>
          )}
        </div>
      </div>

      {/* CONFIRM ENROLLMENT DIALOG */}
      <ConfirmDialog
        isOpen={showConfirmModal}
        onClose={() => setShowConfirmModal(false)}
        onConfirm={handleConfirmEnrollment}
        title="Confirm Pathway Selection"
        description={`Select ${pathway.title} as your primary active livelihood pathway and save it to your beneficiary dashboard?`}
        confirmText="Confirm Selection"
        variant="default"
      />
    </div>
  );
};
