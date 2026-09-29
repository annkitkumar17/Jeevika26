import { useState } from 'react';
import { useAppStore } from '../stores/useAppStore';
import { GeoLocation } from '../types';

export function useGeolocation() {
  const { userLocation, setUserLocation } = useAppStore();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const requestGeolocation = () => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser.');
      return;
    }

    setLoading(true);
    setError(null);

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const newLocation: GeoLocation = {
          state: userLocation?.state || 'Uttar Pradesh',
          district: userLocation?.district || 'Lucknow',
          block: userLocation?.block || 'Sadar',
          village: 'User Geolocated Site',
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          dataStatus: 'user_geolocated',
        };
        setUserLocation(newLocation);
        setLoading(false);
      },
      (err) => {
        setLoading(false);
        if (err.code === err.PERMISSION_DENIED) {
          setError('Location permission was denied. Using manual/default location.');
        } else {
          setError('Could not retrieve location. Using manual/default location.');
        }
      },
      { timeout: 10000, enableHighAccuracy: false }
    );
  };

  const updateManualLocation = (district: string, block: string, village: string) => {
    // Fictional default coordinates for Lucknow district blocks
    const newLoc: GeoLocation = {
      state: 'Uttar Pradesh',
      district,
      block,
      village,
      latitude: 26.8467,
      longitude: 80.9462,
      dataStatus: 'demo_seeded',
    };
    setUserLocation(newLoc);
    setError(null);
  };

  return {
    location: userLocation,
    loading,
    error,
    requestGeolocation,
    updateManualLocation,
  };
}
