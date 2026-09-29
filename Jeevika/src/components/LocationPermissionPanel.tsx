import React, { useState } from 'react';
import { MapPin, Navigation, Check, AlertTriangle } from 'lucide-react';
import { Button } from './ui/Button';
import { useGeolocation } from '../hooks/useGeolocation';

interface LocationPermissionPanelProps {
  onLocationConfirmed?: () => void;
  className?: string;
}

export const LocationPermissionPanel: React.FC<LocationPermissionPanelProps> = ({
  onLocationConfirmed,
  className = '',
}) => {
  const { location, loading, error, requestGeolocation, updateManualLocation } = useGeolocation();
  const [showManualForm, setShowManualForm] = useState(false);

  const [district, setDistrict] = useState(location?.district || 'Lucknow');
  const [block, setBlock] = useState(location?.block || 'Sadar');
  const [village, setVillage] = useState(location?.village || 'Rampur Demo');

  const handleManualSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    updateManualLocation(district, block, village);
    setShowManualForm(false);
    if (onLocationConfirmed) onLocationConfirmed();
  };

  return (
    <div className={`p-5 rounded-2xl bg-white border border-slate-200 shadow-sm ${className}`}>
      <div className="flex items-start gap-3">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-brand-100 text-brand-700">
          <MapPin className="h-5 w-5" />
        </div>
        <div className="flex-1">
          <h4 className="font-bold text-slate-900 text-sm">Location Preference</h4>
          <p className="text-xs text-slate-600 mt-0.5">
            We use your location solely to calculate distance to nearby PMKK / JSS training centres.
          </p>

          <div className="mt-3 p-2.5 rounded-lg bg-slate-50 border border-slate-100 text-xs text-slate-700">
            Current Location:{' '}
            <strong className="text-slate-900">
              {location?.village}, {location?.block}, {location?.district}, {location?.state}
            </strong>
            <span className="ml-2 text-[10px] text-brand-700 font-semibold bg-brand-50 px-1.5 py-0.5 rounded">
              {location?.dataStatus === 'user_geolocated' ? 'GPS Geolocated' : 'Seeded Demo'}
            </span>
          </div>

          {error && (
            <div className="flex items-center gap-2 mt-2 text-xs text-amber-800 bg-amber-50 p-2 rounded-lg border border-amber-200">
              <AlertTriangle className="h-4 w-4 shrink-0 text-amber-600" />
              <span>{error}</span>
            </div>
          )}

          {!showManualForm ? (
            <div className="flex flex-wrap items-center gap-2 mt-4">
              <Button
                variant="default"
                size="sm"
                onClick={() => {
                  requestGeolocation();
                  if (onLocationConfirmed) onLocationConfirmed();
                }}
                disabled={loading}
                className="gap-2 text-xs"
              >
                <Navigation className="h-3.5 w-3.5" />
                <span>{loading ? 'Locating...' : 'Use Browser GPS'}</span>
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => setShowManualForm(true)}
                className="text-xs"
              >
                Select District / Block Manually
              </Button>
            </div>
          ) : (
            <form onSubmit={handleManualSubmit} className="mt-4 space-y-3 pt-3 border-t border-slate-100">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                <div>
                  <label className="text-[11px] font-semibold text-slate-500">District</label>
                  <input
                    type="text"
                    value={district}
                    onChange={(e) => setDistrict(e.target.value)}
                    className="w-full p-2 rounded-lg border text-xs focus:ring-2 focus:ring-brand-500"
                    required
                  />
                </div>
                <div>
                  <label className="text-[11px] font-semibold text-slate-500">Block</label>
                  <input
                    type="text"
                    value={block}
                    onChange={(e) => setBlock(e.target.value)}
                    className="w-full p-2 rounded-lg border text-xs focus:ring-2 focus:ring-brand-500"
                    required
                  />
                </div>
                <div>
                  <label className="text-[11px] font-semibold text-slate-500">Village / GP</label>
                  <input
                    type="text"
                    value={village}
                    onChange={(e) => setVillage(e.target.value)}
                    className="w-full p-2 rounded-lg border text-xs focus:ring-2 focus:ring-brand-500"
                    required
                  />
                </div>
              </div>
              <div className="flex justify-end gap-2">
                <Button variant="ghost" size="sm" onClick={() => setShowManualForm(false)}>
                  Cancel
                </Button>
                <Button type="submit" variant="default" size="sm" className="gap-1">
                  <Check className="h-3.5 w-3.5" /> Save Location
                </Button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};
