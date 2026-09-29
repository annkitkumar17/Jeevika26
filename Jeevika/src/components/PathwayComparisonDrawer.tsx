import React from 'react';
import { AlertCircle, CheckCircle2, XCircle } from 'lucide-react';
import { Drawer } from './ui/Drawer';
import { Badge } from './ui/Badge';
import { Button } from './ui/Button';
import { PathwayRecommendation } from '../types';
import { formatDistanceDemo } from '../lib/geo';

interface PathwayComparisonDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  pathways: PathwayRecommendation[];
  onSelectPathway: (id: string) => void;
}

export const PathwayComparisonDrawer: React.FC<PathwayComparisonDrawerProps> = ({
  isOpen,
  onClose,
  pathways,
  onSelectPathway,
}) => {
  return (
    <Drawer
      isOpen={isOpen}
      onClose={onClose}
      title="Compare Livelihood Pathways"
      side="bottom"
      className="max-w-5xl mx-auto"
    >
      <div className="space-y-4">
        <div className="p-3 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-xs flex items-start gap-2">
          <AlertCircle className="h-4 w-4 text-amber-600 shrink-0 mt-0.5" />
          <div>
            <strong>Facilitator Verification Notice:</strong> All AI recommendations require local verification by your PM-AJAY Block Facilitator before formal training enrolment or grant disbursement.
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50">
                <th className="p-3 font-semibold text-slate-500 w-36">Criteria</th>
                {pathways.map((p) => (
                  <th key={p.id} className="p-3 font-bold text-slate-900 min-w-[220px]">
                    <div className="flex items-center gap-2 mb-1">
                      <Badge variant="saffron" className="text-[10px]">Rank #{p.rank}</Badge>
                      <span className="text-emerald-700 font-bold">{p.suitabilityScore}% Fit</span>
                    </div>
                    <div>{p.title}</div>
                    <div className="text-[10px] text-slate-400 font-normal">NSQF Level {p.nsqfLevel}</div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              <tr>
                <td className="p-3 font-semibold text-slate-600 bg-slate-50/50">Skill Match & Sector</td>
                {pathways.map((p) => (
                  <td key={p.id} className="p-3 text-slate-700">
                    <div className="font-medium text-slate-900">{p.sector}</div>
                    <div className="text-[11px] text-slate-500 mt-1">{p.fitReason}</div>
                  </td>
                ))}
              </tr>
              <tr>
                <td className="p-3 font-semibold text-slate-600 bg-slate-50/50">Travel & Distance</td>
                {pathways.map((p) => (
                  <td key={p.id} className="p-3 text-slate-700">
                    <div className="font-semibold">{formatDistanceDemo(p.nearestCentre.distanceKm)}</div>
                    <div className="text-[11px] text-slate-500">{p.nearestCentre.name}</div>
                  </td>
                ))}
              </tr>
              <tr>
                <td className="p-3 font-semibold text-slate-600 bg-slate-50/50">Duration & Earnings</td>
                {pathways.map((p) => (
                  <td key={p.id} className="p-3 text-slate-700">
                    <div><strong>{p.durationWeeks} Weeks</strong> course</div>
                    <div className="text-emerald-700 font-semibold mt-0.5">{p.estimatedEarnings}</div>
                  </td>
                ))}
              </tr>
              <tr>
                <td className="p-3 font-semibold text-slate-600 bg-slate-50/50">RPL Possibility</td>
                {pathways.map((p) => (
                  <td key={p.id} className="p-3 text-slate-700">
                    {p.rplEligible ? (
                      <span className="inline-flex items-center gap-1 text-emerald-700 font-semibold">
                        <CheckCircle2 className="h-4 w-4" /> Eligible (Fast-track)
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 text-slate-400">
                        <XCircle className="h-4 w-4" /> Full Training Required
                      </span>
                    )}
                  </td>
                ))}
              </tr>
              <tr>
                <td className="p-3 font-semibold text-slate-600 bg-slate-50/50">Key Risk / Warning</td>
                {pathways.map((p) => (
                  <td key={p.id} className="p-3 text-amber-900 bg-amber-50/50">
                    {p.riskWarning || 'Standard safety requirements'}
                  </td>
                ))}
              </tr>
              <tr>
                <td className="p-3 font-semibold text-slate-600 bg-slate-50/50">Action</td>
                {pathways.map((p) => (
                  <td key={p.id} className="p-3">
                    <Button
                      variant="default"
                      size="sm"
                      onClick={() => {
                        onSelectPathway(p.id);
                        onClose();
                      }}
                      className="w-full text-xs"
                    >
                      Select Pathway #{p.rank}
                    </Button>
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </Drawer>
  );
};
