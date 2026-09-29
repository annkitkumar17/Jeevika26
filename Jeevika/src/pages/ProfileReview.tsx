import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  UserCheck,
  Edit3,
  Sparkles,
  ArrowRight,
  Briefcase,
  GraduationCap,
  Wrench,
  Compass,
  MapPin,
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Modal } from '../components/ui/Modal';
import { ConfidenceMeter } from '../components/ConfidenceMeter';
import { DemoDataBadge } from '../components/DemoDataBadge';
import { LocationPermissionPanel } from '../components/LocationPermissionPanel';
import { useAppStore } from '../stores/useAppStore';
import { useRecommendations } from '../hooks/useRecommendations';

export const ProfileReview: React.FC = () => {
  const navigate = useNavigate();
  const { profile, setProfile, answers } = useAppStore();
  const { generateProfile } = useRecommendations();

  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  // Fallback demo profile if null
  const currentProfile = profile || {
    id: 'ben-demo-001',
    name: 'Rajesh Kumar',
    phone: '+91 98765 43210',
    language: 'hi' as const,
    gender: 'Male',
    age: 24,
    category: 'SC (PM-AJAY beneficiary)',
    location: {
      state: 'Uttar Pradesh',
      district: 'Lucknow',
      block: 'Sadar',
      village: 'Rampur Demo',
      latitude: 26.8467,
      longitude: 80.9462,
      dataStatus: 'demo_seeded' as const,
    },
    education: answers['education'] || 'Class 10 Passed',
    currentWork: answers['currentWork'] || 'Assists with agricultural pump repair',
    workExperienceYears: 2,
    skills: ['Basic mechanical repair', 'Tool handling', 'Customer interaction'],
    aspirations: answers['interestArea'] || 'Solar PV installation & repair business',
    preferences: {
      employmentType: 'self_employment' as const,
      maxTravelKm: 25,
      migration: false,
      hasVehicle: true,
    },
    extractedProfile: {
      educationLevel: answers['education'] || 'Class 10 Passed',
      primarySkillSet: answers['currentWork'] || 'Mechanical & Pump Repair',
      yearsExperience: '2 years informal',
      mobilityPreference: 'Up to 25 km (District block level)',
      preferredOutcome: answers['employmentType'] || 'Self-employment / Micro-enterprise',
      confidenceScore: 92,
      dataStatus: 'demo_seeded' as const,
    },
    enrolledPathwayId: null,
    status: 'profile_confirmed' as const,
  };

  // Editable local state for modal
  const [formData, setFormData] = useState({
    name: currentProfile.name,
    education: currentProfile.education,
    currentWork: currentProfile.currentWork,
    aspirations: currentProfile.aspirations,
    employmentType: currentProfile.preferences.employmentType,
    maxTravelKm: currentProfile.preferences.maxTravelKm,
  });

  const handleSaveProfileEdit = () => {
    const updated = {
      ...currentProfile,
      name: formData.name,
      education: formData.education,
      currentWork: formData.currentWork,
      aspirations: formData.aspirations,
      preferences: {
        ...currentProfile.preferences,
        employmentType: formData.employmentType,
        maxTravelKm: Number(formData.maxTravelKm),
      },
    };
    setProfile(updated);
    setIsEditModalOpen(false);
  };

  const handleFindPathways = () => {
    navigate('/recommendations');
  };

  return (
    <div className="max-w-4xl mx-auto py-6 px-4 space-y-8">
      {/* HEADER */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-white border border-slate-200 shadow-sm">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold text-slate-900">Extracted Beneficiary Profile</h1>
            <DemoDataBadge text="Seeded Demo Profile" />
          </div>
          <p className="text-xs text-slate-500">
            Confirm your AI-extracted skill parameters before generating ranked NSQF pathways.
          </p>
        </div>

        <Button
          variant="outline"
          size="sm"
          onClick={() => setIsEditModalOpen(true)}
          className="gap-2 text-xs self-start md:self-auto"
        >
          <Edit3 className="h-4 w-4" />
          <span>Edit Extracted Fields</span>
        </Button>
      </div>

      {/* CONFIDENCE METER */}
      <ConfidenceMeter score={currentProfile.extractedProfile.confidenceScore} />

      {/* PROFILE CARDS GRID */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Education & Experience */}
        <Card className="bg-white border-slate-200">
          <CardHeader className="flex flex-row items-center gap-3 p-0 mb-4">
            <div className="p-2.5 rounded-xl bg-brand-100 text-brand-700">
              <GraduationCap className="h-5 w-5" />
            </div>
            <div>
              <CardTitle className="text-base font-bold text-slate-900">Education & Background</CardTitle>
              <span className="text-xs text-slate-400">Formal qualification pack prerequisites</span>
            </div>
          </CardHeader>
          <CardContent className="p-0 space-y-3 text-xs">
            <div className="flex justify-between py-1.5 border-b border-slate-100">
              <span className="text-slate-500">Highest Education:</span>
              <span className="font-bold text-slate-900">{currentProfile.education}</span>
            </div>
            <div className="flex justify-between py-1.5 border-b border-slate-100">
              <span className="text-slate-500">Current / Previous Work:</span>
              <span className="font-bold text-slate-900 text-right">{currentProfile.currentWork}</span>
            </div>
            <div className="flex justify-between py-1.5">
              <span className="text-slate-500">Category / Scheme:</span>
              <span className="font-semibold text-brand-700">{currentProfile.category}</span>
            </div>
          </CardContent>
        </Card>

        {/* Existing Skills & Aspirations */}
        <Card className="bg-white border-slate-200">
          <CardHeader className="flex flex-row items-center gap-3 p-0 mb-4">
            <div className="p-2.5 rounded-xl bg-saffron-100 text-saffron-700">
              <Wrench className="h-5 w-5" />
            </div>
            <div>
              <CardTitle className="text-base font-bold text-slate-900">Extracted Skills & Aspirations</CardTitle>
              <span className="text-xs text-slate-400">Matched with RPL assessment standards</span>
            </div>
          </CardHeader>
          <CardContent className="p-0 space-y-3 text-xs">
            <div>
              <span className="text-slate-500 block mb-1.5">Existing Practical Skills:</span>
              <div className="flex flex-wrap gap-1.5">
                {currentProfile.skills.map((skill, i) => (
                  <Badge key={i} variant="default" className="text-[11px]">
                    {skill}
                  </Badge>
                ))}
              </div>
            </div>
            <div className="pt-2 border-t border-slate-100">
              <span className="text-slate-500 block mb-1">Target Aspirations:</span>
              <p className="font-semibold text-slate-800 leading-relaxed">{currentProfile.aspirations}</p>
            </div>
          </CardContent>
        </Card>

        {/* Mobility & Preference */}
        <Card className="bg-white border-slate-200 md:col-span-2">
          <CardHeader className="flex flex-row items-center gap-3 p-0 mb-4">
            <div className="p-2.5 rounded-xl bg-emerald-100 text-emerald-700">
              <Compass className="h-5 w-5" />
            </div>
            <div>
              <CardTitle className="text-base font-bold text-slate-900">Mobility & Employment Preference</CardTitle>
              <span className="text-xs text-slate-400">Used for local training centre distance calculation</span>
            </div>
          </CardHeader>
          <CardContent className="p-0 grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
              <span className="text-slate-500 block text-[11px]">Employment Mode</span>
              <span className="font-bold text-slate-900 text-sm capitalize">
                {currentProfile.preferences.employmentType.replace('_', ' ')}
              </span>
            </div>
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
              <span className="text-slate-500 block text-[11px]">Max Travel Radius</span>
              <span className="font-bold text-slate-900 text-sm">
                Up to {currentProfile.preferences.maxTravelKm} km
              </span>
            </div>
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
              <span className="text-slate-500 block text-[11px]">Migration Willingness</span>
              <span className="font-bold text-slate-900 text-sm">
                {currentProfile.preferences.migration ? 'Willing to Migrate' : 'Local District Only'}
              </span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* LOCATION PERMISSION PANEL */}
      <LocationPermissionPanel />

      {/* PRIMARY CTA */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-brand-900 to-slate-900 text-white flex flex-col sm:flex-row items-center justify-between gap-4 shadow-xl">
        <div className="space-y-1 text-center sm:text-left">
          <h3 className="text-lg font-bold">Ready to discover your 3 recommended pathways?</h3>
          <p className="text-xs text-slate-300">
            Matches your profile against local PMKK centres in {currentProfile.location.district}.
          </p>
        </div>
        <Button
          variant="accent"
          size="lg"
          onClick={handleFindPathways}
          className="w-full sm:w-auto gap-2 text-slate-900 font-extrabold px-8 shrink-0 shadow-lg"
        >
          <span>Find My Pathways</span>
          <ArrowRight className="h-5 w-5" />
        </Button>
      </div>

      {/* EDIT MODAL */}
      <Modal
        isOpen={isEditModalOpen}
        onClose={() => setIsEditModalOpen(false)}
        title="Edit Beneficiary Profile Fields"
        description="Update profile values used by local mock recommendation engine."
      >
        <div className="space-y-4 pt-2 text-xs">
          <div>
            <label className="font-bold text-slate-700 block mb-1">Beneficiary Name</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full p-2.5 rounded-lg border text-sm focus:ring-2 focus:ring-brand-500"
            />
          </div>
          <div>
            <label className="font-bold text-slate-700 block mb-1">Education Level</label>
            <input
              type="text"
              value={formData.education}
              onChange={(e) => setFormData({ ...formData, education: e.target.value })}
              className="w-full p-2.5 rounded-lg border text-sm focus:ring-2 focus:ring-brand-500"
            />
          </div>
          <div>
            <label className="font-bold text-slate-700 block mb-1">Current Work Experience</label>
            <textarea
              value={formData.currentWork}
              onChange={(e) => setFormData({ ...formData, currentWork: e.target.value })}
              className="w-full p-2.5 rounded-lg border text-sm focus:ring-2 focus:ring-brand-500"
              rows={2}
            />
          </div>
          <div>
            <label className="font-bold text-slate-700 block mb-1">Target Aspirations</label>
            <input
              type="text"
              value={formData.aspirations}
              onChange={(e) => setFormData({ ...formData, aspirations: e.target.value })}
              className="w-full p-2.5 rounded-lg border text-sm focus:ring-2 focus:ring-brand-500"
            />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="font-bold text-slate-700 block mb-1">Employment Mode</label>
              <select
                value={formData.employmentType}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    employmentType: e.target.value as any,
                  })
                }
                className="w-full p-2.5 rounded-lg border text-xs focus:ring-2 focus:ring-brand-500"
              >
                <option value="self_employment">Self Employment</option>
                <option value="wage_employment">Wage Employment</option>
                <option value="either">Either</option>
              </select>
            </div>
            <div>
              <label className="font-bold text-slate-700 block mb-1">Max Travel (km)</label>
              <input
                type="number"
                value={formData.maxTravelKm}
                onChange={(e) => setFormData({ ...formData, maxTravelKm: Number(e.target.value) })}
                className="w-full p-2.5 rounded-lg border text-xs focus:ring-2 focus:ring-brand-500"
              />
            </div>
          </div>
          <div className="flex justify-end gap-2 pt-3 border-t">
            <Button variant="secondary" size="sm" onClick={() => setIsEditModalOpen(false)}>
              Cancel
            </Button>
            <Button variant="default" size="sm" onClick={handleSaveProfileEdit}>
              Save Profile Changes
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};
