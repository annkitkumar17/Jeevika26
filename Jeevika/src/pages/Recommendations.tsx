import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Layers, Bookmark, AlertCircle, Compass } from 'lucide-react';
import { PathwayCard } from '../components/PathwayCard';
import { PathwayComparisonDrawer } from '../components/PathwayComparisonDrawer';
import { DemoDataBadge } from '../components/DemoDataBadge';
import { Button } from '../components/ui/Button';
import { useRecommendations } from '../hooks/useRecommendations';
import { useAppStore } from '../stores/useAppStore';
import { PathwayRecommendation } from '../types';

export const Recommendations: React.FC = () => {
  const navigate = useNavigate();
  const { recommendations, isLoading } = useRecommendations();
  const { savedPathwayIds, toggleSavePathway, setSelectedPathwayId } = useAppStore();

  const [isCompareDrawerOpen, setIsCompareDrawerOpen] = useState(false);

  const handleSelectPathway = (id: string) => {
    setSelectedPathwayId(id);
    navigate(`/pathway/${id}`);
  };

  return (
    <div className="max-w-7xl mx-auto py-6 px-4 space-y-8">
      {/* HEADER */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-white border border-slate-200 shadow-sm">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold text-slate-900">Recommended Livelihood Pathways</h1>
            <DemoDataBadge text="NSQF Aligned" />
          </div>
          <p className="text-xs text-slate-500">
            Ranked based on your voice profile, past repair experience, and nearby Sadar PMKK availability.
          </p>
        </div>

        <Button
          variant="accent"
          size="sm"
          onClick={() => setIsCompareDrawerOpen(true)}
          className="gap-2 font-bold text-slate-900 shrink-0"
        >
          <Layers className="h-4 w-4" />
          <span>Compare 3 Pathways</span>
        </Button>
      </div>

      {/* VERIFICATION NOTICE */}
      <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-xs flex items-start gap-3">
        <AlertCircle className="h-5 w-5 text-amber-600 shrink-0 mt-0.5" />
        <div>
          <strong className="font-bold">Facilitator Verification Protocol:</strong> These initial recommendations are generated locally using seeded PM-AJAY micro-enterprise rules. A local block facilitator must inspect original documents and confirm eligibility before official batch enrollment.
        </div>
      </div>

      {/* PATHWAY CARDS GRID */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-96 rounded-2xl bg-slate-200 animate-pulse" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {recommendations.map((pathway) => (
            <PathwayCard
              key={pathway.id}
              pathway={pathway}
              onSelect={handleSelectPathway}
              onCompare={() => setIsCompareDrawerOpen(true)}
              onToggleSave={toggleSavePathway}
              isSaved={savedPathwayIds.includes(pathway.id)}
            />
          ))}
        </div>
      )}

      {/* COMPARISON DRAWER */}
      <PathwayComparisonDrawer
        isOpen={isCompareDrawerOpen}
        onClose={() => setIsCompareDrawerOpen(false)}
        pathways={recommendations}
        onSelectPathway={handleSelectPathway}
      />
    </div>
  );
};
