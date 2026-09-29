import React from 'react';
import { Sparkles, MapPin, Award, ArrowRight, Bookmark, AlertCircle, Layers } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from './ui/Card';
import { Badge } from './ui/Badge';
import { Button } from './ui/Button';
import { SkillGapChip } from './SkillGapChip';
import { DemoDataBadge } from './DemoDataBadge';
import { PathwayRecommendation } from '../types';
import { formatDistanceDemo } from '../lib/geo';

interface PathwayCardProps {
  pathway: PathwayRecommendation;
  onSelect: (id: string) => void;
  onCompare?: (pathway: PathwayRecommendation) => void;
  onToggleSave?: (id: string) => void;
  isSaved?: boolean;
}

export const PathwayCard: React.FC<PathwayCardProps> = ({
  pathway,
  onSelect,
  onCompare,
  onToggleSave,
  isSaved = false,
}) => {
  return (
    <Card hoverEffect className="relative flex flex-col justify-between h-full bg-white border-slate-200">
      <div>
        <div className="flex items-center justify-between gap-2 mb-3">
          <div className="flex items-center gap-2">
            <Badge variant="saffron" className="font-bold text-xs px-3 py-1">
              Rank #{pathway.rank}
            </Badge>
            <Badge variant="default" className="text-xs">
              NSQF Level {pathway.nsqfLevel}
            </Badge>
          </div>
          <div className="flex items-center gap-1 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200 text-emerald-800 text-xs font-bold">
            <Sparkles className="h-3.5 w-3.5 text-emerald-600" />
            <span>{pathway.suitabilityScore}% Fit Score</span>
          </div>
        </div>

        <CardHeader className="p-0 mb-3">
          <CardTitle className="text-xl font-bold text-slate-900 leading-snug">
            {pathway.title}
          </CardTitle>
          <div className="flex items-center gap-2 text-xs text-slate-500 font-medium mt-1">
            <span>QP Code: {pathway.qpCode}</span>
            <span>•</span>
            <span className="text-brand-700 font-semibold">{pathway.sector}</span>
          </div>
        </CardHeader>

        <CardContent className="p-0 space-y-4">
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-100 text-xs text-slate-700 leading-relaxed">
            <div className="font-semibold text-slate-900 mb-1 flex items-center gap-1.5">
              <Sparkles className="h-3.5 w-3.5 text-brand-600" />
              Why this pathway fits your profile:
            </div>
            <p>{pathway.fitReason}</p>
          </div>

          {/* Skill gaps & bridge modules */}
          <div>
            <div className="text-xs font-semibold text-slate-500 mb-2">
              Identified Skill Gaps & Bridge Modules:
            </div>
            <div className="flex flex-wrap gap-1.5">
              {pathway.skillGaps.map((gap, i) => (
                <SkillGapChip key={i} gapText={gap} />
              ))}
            </div>
          </div>

          {/* Demo training centre fit */}
          <div className="flex items-center justify-between text-xs text-slate-600 pt-2 border-t border-slate-100">
            <div className="flex items-center gap-1.5 truncate">
              <MapPin className="h-3.5 w-3.5 text-brand-600 shrink-0" />
              <span className="truncate">{pathway.nearestCentre.name}</span>
            </div>
            <span className="font-semibold shrink-0 text-brand-900 bg-slate-100 px-2 py-0.5 rounded-md">
              {formatDistanceDemo(pathway.nearestCentre.distanceKm)}
            </span>
          </div>

          {/* Local demand signal */}
          <div className="flex items-center justify-between text-xs p-2.5 rounded-lg bg-slate-100/70">
            <span className="text-slate-500">Local Opportunity Signal:</span>
            <div className="flex items-center gap-1.5">
              <span className="font-bold text-slate-800">{pathway.localDemandSignal}</span>
              <DemoDataBadge text="Demo signal" className="py-0 px-1.5 text-[10px]" />
            </div>
          </div>

          {/* Risk Warning */}
          {pathway.riskWarning && (
            <div className="flex items-start gap-2 p-2.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-xs">
              <AlertCircle className="h-4 w-4 shrink-0 text-amber-600 mt-0.5" />
              <span>{pathway.riskWarning}</span>
            </div>
          )}
        </CardContent>
      </div>

      <CardFooter className="p-0 pt-4 mt-6 border-t border-slate-100 flex flex-col gap-2">
        <div className="flex items-center justify-between w-full text-xs text-slate-500">
          <span>Duration: <strong>{pathway.durationWeeks} Weeks</strong></span>
          <span>Earnings: <strong>{pathway.estimatedEarnings}</strong></span>
        </div>
        <div className="flex items-center gap-2 w-full mt-2">
          {onCompare && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => onCompare(pathway)}
              className="gap-1 text-xs px-2.5"
            >
              <Layers className="h-3.5 w-3.5" />
              Compare
            </Button>
          )}
          {onToggleSave && (
            <Button
              variant={isSaved ? 'accent' : 'ghost'}
              size="sm"
              onClick={() => onToggleSave(pathway.id)}
              className="px-2.5"
              title={isSaved ? 'Saved for later' : 'Save for later'}
            >
              <Bookmark className={`h-3.5 w-3.5 ${isSaved ? 'fill-slate-900' : ''}`} />
            </Button>
          )}
          <Button
            variant="default"
            size="sm"
            onClick={() => onSelect(pathway.id)}
            className="flex-1 gap-2 text-xs font-semibold"
          >
            <span>See Pathway Detail</span>
            <ArrowRight className="h-3.5 w-3.5" />
          </Button>
        </div>
      </CardFooter>
    </Card>
  );
};
