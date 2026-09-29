import { describe, it, expect, beforeEach } from 'vitest';
import { calculateHaversineDistanceKm, estimateTravelTimeMinutes } from '../lib/geo';
import { useAppStore } from '../stores/useAppStore';

describe('Jeevika Saarthi AI Unit Tests', () => {
  beforeEach(() => {
    useAppStore.getState().resetEntireDemo();
  });

  // Test 1: Haversine distance utility
  it('calculates Haversine distance accurately between two coordinates', () => {
    // Distance between Sadar Lucknow (26.8467, 80.9462) and PMKK Sadar (26.8520, 80.9580)
    const dist = calculateHaversineDistanceKm(26.8467, 80.9462, 26.852, 80.958);
    expect(dist).toBeGreaterThan(0.5);
    expect(dist).toBeLessThan(3.0);
  });

  // Test 2: Travel time estimator
  it('estimates travel time based on distance', () => {
    const time = estimateTravelTimeMinutes(10);
    expect(time).toBe(24);
  });

  // Test 3: Language persistence in store
  it('updates and persists selected language in Zustand store', () => {
    const store = useAppStore.getState();
    expect(store.language).toBe('hi');

    store.setLanguage('mr');
    expect(useAppStore.getState().language).toBe('mr');
  });

  // Test 4: Consent state enforcement
  it('manages consent completion correctly', () => {
    const store = useAppStore.getState();
    expect(store.consent.profileCreation).toBe(false);

    store.setConsent({ profileCreation: true, recommendations: true });
    store.completeConsent();

    expect(useAppStore.getState().consent.completedAt).not.toBeNull();
  });

  // Test 5: Reduced motion setting toggle
  it('toggles reduced motion setting in app store', () => {
    const store = useAppStore.getState();
    expect(store.reducedMotion).toBe(false);

    store.setReducedMotion(true);
    expect(useAppStore.getState().reducedMotion).toBe(true);
  });

  // Test 6: Pathway selection updates state
  it('updates enrolled pathway ID in store', () => {
    const store = useAppStore.getState();
    expect(store.selectedPathwayId).toBeNull();

    store.setEnrolledPathway('pathway-solar-tech');
    expect(useAppStore.getState().selectedPathwayId).toBe('pathway-solar-tech');
  });

  // Test 7: Conversation progress & answer storing
  it('stores interview answers and advances current question index', () => {
    const store = useAppStore.getState();
    expect(store.currentQuestionIndex).toBe(0);

    store.setAnswer('currentWork', 'Solar Pump Repair');
    store.nextQuestion();

    expect(useAppStore.getState().answers['currentWork']).toBe('Solar Pump Repair');
    expect(useAppStore.getState().currentQuestionIndex).toBe(1);
  });

  // Test 8: Reset entire demo resets state to default
  it('clears conversation state and demo preferences on resetEntireDemo', () => {
    const store = useAppStore.getState();
    store.setAnswer('currentWork', 'Tailoring');
    store.setEnrolledPathway('pathway-food-prep');

    store.resetEntireDemo();

    const resetState = useAppStore.getState();
    expect(resetState.answers).toEqual({});
    expect(resetState.selectedPathwayId).toBeNull();
    expect(resetState.currentQuestionIndex).toBe(0);
  });
});
