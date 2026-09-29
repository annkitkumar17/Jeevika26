import React, { useState } from 'react';
import {
  Users,
  Search,
  Filter,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Bell,
  CheckSquare,
  FileText,
  Phone,
  Building,
  RefreshCw,
} from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Drawer } from '../components/ui/Drawer';
import { DataTable, Column } from '../components/DataTable';
import { MetricCard } from '../components/MetricCard';
import { DemoDataBadge } from '../components/DemoDataBadge';
import { OfflineStatus } from '../components/OfflineStatus';
import { FacilitatorCase } from '../types';
import { mockApi } from '../services/mockApi';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';

export const Facilitator: React.FC = () => {
  const queryClient = useQueryClient();

  const [selectedBlock, setSelectedBlock] = useState('Sadar');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCase, setSelectedCase] = useState<FacilitatorCase | null>(null);

  const { data: cases = [], isLoading } = useQuery({
    queryKey: ['facilitator-cases'],
    queryFn: () => mockApi.fetchFacilitatorCases(),
  });

  const updateStatusMutation = useMutation({
    mutationFn: ({ id, status, notes }: { id: string; status: FacilitatorCase['verificationStatus']; notes?: string }) =>
      mockApi.updateCaseStatus(id, status, notes),
    onSuccess: (updated) => {
      queryClient.invalidateQueries({ queryKey: ['facilitator-cases'] });
      toast.success(`Updated status for ${updated.beneficiaryName} to ${updated.verificationStatus}`);
      if (selectedCase && selectedCase.id === updated.id) {
        setSelectedCase(updated);
      }
    },
  });

  const filteredCases = cases.filter((c) => {
    const matchesBlock = selectedBlock === 'All' || c.block === selectedBlock;
    const matchesSearch =
      c.beneficiaryName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.village.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.recommendedPathway.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesBlock && matchesSearch;
  });

  const metrics = {
    totalAssigned: cases.length,
    pendingReview: cases.filter((c) => c.verificationStatus === 'pending_document_check').length,
    verified: cases.filter((c) => c.verificationStatus === 'verified').length,
    actionRequired: cases.filter((c) => c.verificationStatus === 'action_required').length,
  };

  const columns: Column<FacilitatorCase>[] = [
    {
      header: 'Beneficiary Name',
      accessorKey: 'beneficiaryName',
      cell: (row) => (
        <div>
          <div className="font-bold text-slate-900">{row.beneficiaryName}</div>
          <div className="text-[11px] text-slate-400">{row.phone}</div>
        </div>
      ),
    },
    {
      header: 'Location / GP',
      cell: (row) => (
        <div>
          <div className="font-semibold text-slate-800">{row.village}</div>
          <div className="text-[11px] text-slate-400">{row.block} Block</div>
        </div>
      ),
    },
    {
      header: 'Recommended Pathway',
      accessorKey: 'recommendedPathway',
      cell: (row) => (
        <span className="font-bold text-brand-800 bg-brand-50 px-2.5 py-1 rounded-md">
          {row.recommendedPathway}
        </span>
      ),
    },
    {
      header: 'Status',
      cell: (row) => {
        const variants: Record<FacilitatorCase['verificationStatus'], 'warning' | 'success' | 'destructive' | 'default'> = {
          pending_document_check: 'warning',
          verified: 'success',
          enrolled: 'default',
          action_required: 'destructive',
        };
        return (
          <Badge variant={variants[row.verificationStatus]} className="capitalize">
            {row.verificationStatus.replace(/_/g, ' ')}
          </Badge>
        );
      },
    },
    {
      header: 'Next Follow-up',
      accessorKey: 'nextFollowUpDate',
      cell: (row) => <span className="font-semibold text-slate-700">{row.nextFollowUpDate}</span>,
    },
    {
      header: 'Action',
      cell: (row) => (
        <Button
          variant="outline"
          size="sm"
          onClick={(e) => {
            e.stopPropagation();
            setSelectedCase(row);
          }}
          className="text-xs"
        >
          Review Case
        </Button>
      ),
    },
  ];

  return (
    <div className="max-w-7xl mx-auto py-6 px-4 space-y-8">
      {/* HEADER WITH BLOCK SELECTOR & NOTIFICATIONS */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-white border border-slate-200 shadow-sm">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold text-slate-900">Facilitator Case Management Workspace</h1>
            <DemoDataBadge text="VLE Portal" />
          </div>
          <p className="text-xs text-slate-500">
            Verify beneficiary documents, conduct human review, and dispatch PM-AJAY skilling referrals.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <OfflineStatus />
          <div className="flex items-center gap-2 bg-slate-50 px-3 py-1.5 rounded-xl border border-slate-200 text-xs">
            <Building className="h-4 w-4 text-slate-500" />
            <select
              value={selectedBlock}
              onChange={(e) => setSelectedBlock(e.target.value)}
              className="bg-transparent font-bold text-slate-800 focus:outline-none cursor-pointer"
            >
              <option value="All">All District Blocks</option>
              <option value="Sadar">Sadar Block</option>
              <option value="Chinhat">Chinhat Block</option>
              <option value="Mohanlalganj">Mohanlalganj Block</option>
            </select>
          </div>
          <button
            onClick={() => toast.info('Notification: 2 new document submissions pending review.')}
            className="p-2 rounded-xl border border-slate-200 hover:bg-slate-50 text-slate-600 relative"
            title="Notifications"
          >
            <Bell className="h-5 w-5" />
            <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-rose-500" />
          </button>
        </div>
      </div>

      {/* CASE METRICS */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard
          title="Assigned Beneficiaries"
          value={metrics.totalAssigned}
          subtitle="In selected block"
          icon={Users}
          iconColorClass="bg-brand-100 text-brand-700"
        />
        <MetricCard
          title="Pending Verification"
          value={metrics.pendingReview}
          subtitle="Document check needed"
          icon={Clock}
          iconColorClass="bg-amber-100 text-amber-700"
        />
        <MetricCard
          title="Verified & Ready"
          value={metrics.verified}
          subtitle="Batch eligible"
          icon={CheckCircle2}
          iconColorClass="bg-emerald-100 text-emerald-700"
        />
        <MetricCard
          title="Action Required"
          value={metrics.actionRequired}
          subtitle="Missing bank / Aadhaar"
          icon={AlertTriangle}
          iconColorClass="bg-rose-100 text-rose-700"
        />
      </div>

      {/* FILTERABLE BENEFICIARY CASE TABLE */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="relative flex-1 w-full max-w-md">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by beneficiary name, village or pathway..."
              className="w-full pl-9 pr-4 py-2 rounded-xl border border-slate-200 text-xs focus:ring-2 focus:ring-brand-500"
            />
          </div>
          <div className="text-xs text-slate-500">
            Showing <strong>{filteredCases.length}</strong> of <strong>{cases.length}</strong> cases
          </div>
        </div>

        <DataTable
          columns={columns}
          data={filteredCases}
          onRowClick={(row) => setSelectedCase(row)}
          emptyText="No beneficiary cases matching filter criteria."
        />
      </div>

      {/* BENEFICIARY DETAIL DRAWER */}
      {selectedCase && (
        <Drawer
          isOpen={!!selectedCase}
          onClose={() => setSelectedCase(null)}
          title={`Case Detail: ${selectedCase.beneficiaryName}`}
          side="right"
        >
          <div className="space-y-6 text-xs">
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-100 space-y-2">
              <div className="flex justify-between font-semibold">
                <span className="text-slate-500">Beneficiary ID:</span>
                <span className="text-slate-900">{selectedCase.beneficiaryId}</span>
              </div>
              <div className="flex justify-between font-semibold">
                <span className="text-slate-500">Phone:</span>
                <span className="text-slate-900">{selectedCase.phone}</span>
              </div>
              <div className="flex justify-between font-semibold">
                <span className="text-slate-500">Village & Block:</span>
                <span className="text-slate-900">{selectedCase.village}, {selectedCase.block}</span>
              </div>
            </div>

            {/* Recommended Pathway */}
            <div className="p-4 rounded-xl bg-brand-50 border border-brand-200 space-y-1">
              <span className="text-[11px] font-bold text-brand-800 uppercase">Selected Pathway</span>
              <div className="text-base font-extrabold text-brand-900">{selectedCase.recommendedPathway}</div>
            </div>

            {/* Verification Checklist */}
            <div className="space-y-3">
              <h4 className="font-bold text-slate-900 text-sm flex items-center gap-1.5">
                <CheckSquare className="h-4 w-4 text-brand-600" />
                <span>Facilitator Verification Checklist</span>
              </h4>

              <div className="space-y-2">
                <div className="flex items-center justify-between p-3 rounded-lg border border-slate-200 bg-white">
                  <span>Aadhaar Demo Consent</span>
                  <Badge variant={selectedCase.documentChecklist.aadhaarConsent ? 'success' : 'destructive'}>
                    {selectedCase.documentChecklist.aadhaarConsent ? 'Verified' : 'Missing'}
                  </Badge>
                </div>
                <div className="flex items-center justify-between p-3 rounded-lg border border-slate-200 bg-white">
                  <span>Class 10 / Qualification Marksheet</span>
                  <Badge variant={selectedCase.documentChecklist.class10Certificate ? 'success' : 'destructive'}>
                    {selectedCase.documentChecklist.class10Certificate ? 'Verified' : 'Missing'}
                  </Badge>
                </div>
                <div className="flex items-center justify-between p-3 rounded-lg border border-slate-200 bg-white">
                  <span>Bank Account Details (Jan Dhan)</span>
                  <Badge variant={selectedCase.documentChecklist.bankDetails ? 'success' : 'destructive'}>
                    {selectedCase.documentChecklist.bankDetails ? 'Verified' : 'Missing'}
                  </Badge>
                </div>
              </div>
            </div>

            {/* Risk & Notes */}
            {selectedCase.riskFlag !== 'None' && (
              <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-900">
                <strong>Risk Flag:</strong> {selectedCase.riskFlag}
              </div>
            )}

            {/* Action Buttons */}
            <div className="space-y-2 pt-4 border-t border-slate-100">
              <Button
                variant="default"
                size="default"
                onClick={() =>
                  updateStatusMutation.mutate({ id: selectedCase.id, status: 'verified' })
                }
                className="w-full font-bold bg-emerald-700 hover:bg-emerald-800"
              >
                Approve & Mark Case Verified
              </Button>
              <Button
                variant="secondary"
                size="default"
                onClick={() =>
                  updateStatusMutation.mutate({ id: selectedCase.id, status: 'action_required' })
                }
                className="w-full"
              >
                Request Additional Documents
              </Button>
            </div>
          </div>
        </Drawer>
      )}
    </div>
  );
};
