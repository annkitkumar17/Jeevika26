# Jeevika Saarthi AI - Phase 1 Web Frontend (Localhost)

AI-driven voice assistant for livelihood mapping and NSQF-aligned skilling recommendations under PM-AJAY (Pradhan Mantri Anusuchit Jaati Abhyuday Yojana).

## Overview
Phase 1 delivers a complete, production-quality web application running entirely locally on `http://localhost:3000` with seeded mock data, browser MediaRecorder voice simulation, interactive MapLibre maps, Apache ECharts analytics, and responsive civic-tech design system.

## Tech Stack
- **Framework**: React 18.3, TypeScript 5.5, Vite 5.4
- **Styling**: Tailwind CSS 3.4, Framer Motion 11.3
- **State Management**: Zustand 4.5 (with LocalStorage persistence)
- **Data Fetching**: TanStack React Query 5.52
- **Charts & Maps**: Apache ECharts 5.5, MapLibre GL JS 4.7
- **PWA**: vite-plugin-pwa 0.20
- **Testing**: Vitest 2.0, Testing Library

## Quick Start Commands

```bash
cd apps/web
npm install
npm run dev
# Opens at http://localhost:3000
```

### Running Tests
```bash
npm run test
```

### Production Build Verification
```bash
npm run build
```

## Implemented Pages & Routes
- `/` — Landing page with hero 3D visual, trust strip, 4-step workflow, sample pathways, multi-channel vision.
- `/onboarding` — Language selector (10 Indian languages) & consent panel.
- `/conversation` — 8-step guided voice interview with MediaRecorder & audio simulation fallback.
- `/profile-review` — Extracted profile cards, AI confidence meter & inline editing modal.
- `/recommendations` — 3 ranked NSQF pathways with comparison drawer & save actions.
- `/pathway/:id` — Milestone timeline, nearby PMKK training centres, MapLibre map, and document readiness checklist.
- `/dashboard` — Beneficiary dashboard with selected pathway, upcoming VLE follow-up, and local opportunity list/map toggle.
- `/facilitator` — Facilitator case management workspace with filterable table, review drawer, and verification checklist.
- `/admin` — District analytics dashboard with ECharts visuals, filters, and client-side CSV export.

## Phase 1 Limitations & Seeded Data Notice
All data displayed on the frontend is explicitly labeled with **Demo / locally seeded data** badges (`dataStatus: "demo_seeded"`). No live government APIs, Aadhaar APIs, or remote backend services are called in Phase 1.
