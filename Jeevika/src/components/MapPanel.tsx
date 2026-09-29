import React, { useEffect, useRef, useState } from 'react';
import { Map, Marker, Popup, NavigationControl } from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import { MapPin, Navigation, Building2, CheckCircle2 } from 'lucide-react';
import { GeoLocation, TrainingCentre } from '../types';
import { DemoDataBadge } from './DemoDataBadge';

interface MapPanelProps {
  userLocation?: GeoLocation | null;
  centres?: TrainingCentre[];
  className?: string;
  height?: string;
}

export const MapPanel: React.FC<MapPanelProps> = ({
  userLocation,
  centres = [],
  className = '',
  height = '360px',
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const [mapLoaded, setMapLoaded] = useState(false);

  useEffect(() => {
    if (!mapContainerRef.current) return;

    const centerLat = userLocation?.latitude || 26.8467;
    const centerLng = userLocation?.longitude || 80.9462;

    const map = new Map({
      container: mapContainerRef.current,
      style: {
        version: 8,
        sources: {
          'osm-raster': {
            type: 'raster',
            tiles: [
              'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
            ],
            tileSize: 256,
            attribution: '© OpenStreetMap contributors | PM-AJAY Jeevika Saarthi',
          },
        },
        layers: [
          {
            id: 'osm-raster-layer',
            type: 'raster',
            source: 'osm-raster',
            minzoom: 0,
            maxzoom: 19,
          },
        ],
      },
      center: [centerLng, centerLat],
      zoom: 11.5,
    });

    map.addControl(new NavigationControl({ showCompass: true, showZoom: true }), 'top-right');

    map.on('load', () => {
      setMapLoaded(true);

      // 1. User Location Marker
      const userEl = document.createElement('div');
      userEl.className = 'relative flex items-center justify-center';
      userEl.innerHTML = `
        <div class="absolute -inset-1 rounded-full bg-rose-500 opacity-75 animate-ping"></div>
        <div class="relative flex items-center justify-center h-9 w-9 rounded-full bg-rose-600 text-white shadow-xl ring-2 ring-white font-extrabold text-[11px]">
          YOU
        </div>
      `;

      const userPopup = new Popup({ offset: 25, closeButton: false }).setHTML(`
        <div class="p-2 text-slate-900 font-sans text-xs">
          <div class="font-bold text-slate-900 flex items-center gap-1">📍 Candidate Location</div>
          <div class="text-slate-600 text-[11px]">${userLocation?.village || 'Rampur Demo'}, ${userLocation?.block || 'Sadar'}</div>
        </div>
      `);

      new Marker({ element: userEl })
        .setLngLat([centerLng, centerLat])
        .setPopup(userPopup)
        .addTo(map);

      // 2. Training Centre Markers
      const effectiveCentres = centres.length > 0 ? centres : [
        {
          id: 'tc-01',
          name: 'PMKK Sadar Tech Hub',
          latitude: 26.8520,
          longitude: 80.9520,
          distanceKm: 2.8,
          accreditedSectors: ['Green Jobs / Solar', 'Electronics'],
        },
        {
          id: 'tc-02',
          name: 'Jan Shikshan Sansthan Mohanlalganj',
          latitude: 26.7800,
          longitude: 80.9200,
          distanceKm: 8.4,
          accreditedSectors: ['Agriculture & Food Processing'],
        },
        {
          id: 'tc-03',
          name: 'Govt ITI Alambagh Hub',
          latitude: 26.8200,
          longitude: 80.9100,
          distanceKm: 5.2,
          accreditedSectors: ['Electrical', 'Automotive'],
        },
      ];

      effectiveCentres.forEach((tc, idx) => {
        const tcEl = document.createElement('div');
        tcEl.className = 'flex items-center justify-center h-8 w-8 rounded-full bg-teal-700 text-white shadow-lg ring-2 ring-white font-bold text-[11px] cursor-pointer hover:scale-110 transition-transform';
        tcEl.innerText = `TC${idx + 1}`;

        const tcPopup = new Popup({ offset: 20 }).setHTML(`
          <div class="p-2.5 font-sans space-y-1 text-xs">
            <div class="font-bold text-slate-900">${tc.name}</div>
            <div class="text-emerald-700 font-semibold text-[11px]">Distance: ${tc.distanceKm || '4.5'} km</div>
            <div class="text-slate-500 text-[10px]">${(tc.accreditedSectors || []).join(', ')}</div>
          </div>
        `);

        new Marker({ element: tcEl })
          .setLngLat([tc.longitude, tc.latitude])
          .setPopup(tcPopup)
          .addTo(map);
      });
    });

    return () => {
      map.remove();
    };
  }, [userLocation, centres]);

  return (
    <div
      className={`relative overflow-hidden rounded-2xl border border-slate-200 bg-slate-900 shadow-md ${className}`}
      style={{ height }}
    >
      <div className="absolute top-3 left-3 z-10 flex items-center gap-2">
        <DemoDataBadge text="MapLibre GL JS • OpenStreetMap Vector Engine" className="bg-slate-900/90 text-white border-slate-700" />
      </div>

      <div id="map" ref={mapContainerRef} className="h-full w-full" />
    </div>
  );
};
