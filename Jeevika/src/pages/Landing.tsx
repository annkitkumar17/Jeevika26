import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Mic,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  Sparkles,
  PhoneCall,
  MessageSquare,
  Radio,
  WifiOff,
  Briefcase,
  Award,
  Users,
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { DemoDataBadge } from '../components/DemoDataBadge';
import { VoiceWaveform } from '../components/VoiceWaveform';
import { HeroOrb } from '../components/3d/HeroOrb';
import { useLanguage } from '../hooks/useLanguage';

export const Landing: React.FC = () => {
  const { t } = useLanguage();

  const trustBadges = [
    { title: t('voiceFirst', 'Voice-First Assisted'), icon: Mic },
    { title: t('regionalLanguages', '10 Regional Languages'), icon: Users },
    { title: t('nsqfAligned', 'NSQF-Aligned Pathways'), icon: Award },
    { title: t('humanVerified', 'Human Facilitator Review'), icon: ShieldCheck },
  ];

  const steps = [
    {
      num: '01',
      title: 'Speak',
      desc: 'Answer guided questions about your experience and interests in your natural local dialect.',
    },
    {
      num: '02',
      title: 'Understand',
      desc: 'AI maps your informal skills to standardized National Skills Qualifications Framework (NSQF) levels.',
    },
    {
      num: '03',
      title: 'Match',
      desc: 'Receive three ranked livelihood pathways with nearby PMKK / JSS training centre availability.',
    },
    {
      num: '04',
      title: 'Move Forward',
      desc: 'Connect with a local VLE facilitator for verification, stipend support, and loan linkage.',
    },
  ];

  const samplePathways = [
    {
      id: 'pathway-solar-tech',
      title: 'Solar Pump Technician',
      nsqf: 'Level 3',
      sector: 'Green Energy & Electronics',
      fitScore: 94,
      journeyTime: '6 Weeks',
      fitBadge: 'High Local Fit (PM-KUSUM)',
      desc: 'Assembles and maintains rural solar agricultural water pumping systems.',
    },
    {
      id: 'pathway-food-prep',
      title: 'Food Processing Entrepreneur',
      nsqf: 'Level 4',
      sector: 'Food Processing & Agribusiness',
      fitScore: 86,
      journeyTime: '8 Weeks',
      fitBadge: 'PM-AJAY Capital Grant Fit',
      desc: 'Processes and packages local pulse and spice crops for regional market supply.',
    },
    {
      id: 'pathway-sewing-spec',
      title: 'Sewing Machine Operator',
      nsqf: 'Level 3',
      sector: 'Apparel & Textiles',
      fitScore: 78,
      journeyTime: '5 Weeks',
      fitBadge: 'Immediate Wage Linkage',
      desc: 'Operates industrial single-needle lockstitch machines for garment export units.',
    },
  ];

  return (
    <div className="space-y-20 pb-16">
      {/* HERO SECTION */}
      <section className="relative overflow-hidden pt-12 pb-16 lg:pt-20 lg:pb-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            {/* Left Column: Copy & Actions */}
            <div className="lg:col-span-7 space-y-6">
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-100 border border-brand-200 text-brand-800 text-xs font-semibold">
                <Sparkles className="h-3.5 w-3.5 text-brand-600" />
                <span>PM-AJAY GIA Component AI Skilling Platform</span>
                <DemoDataBadge text="Phase 1 Demo" className="py-0 px-1.5 text-[9px]" />
              </div>

              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-slate-900 leading-[1.15]">
                Your Voice.{' '}
                <span className="bg-gradient-to-r from-brand-700 via-brand-600 to-saffron-600 bg-clip-text text-transparent">
                  Your Livelihood Pathway.
                </span>
              </h1>

              <p className="text-base sm:text-lg text-slate-600 max-w-2xl leading-relaxed">
                Empowering SC community beneficiaries under PM-AJAY through natural voice conversation in Indian languages. Discover NSQF-aligned skilling, RPL certification, and local micro-enterprise pathways.
              </p>

              <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 pt-2">
                <Link to="/onboarding">
                  <Button variant="accent" size="xl" className="w-full sm:w-auto gap-3 text-slate-900 font-bold shadow-xl">
                    <Mic className="h-6 w-6 text-slate-900" />
                    <span>Start Voice Interview</span>
                    <ArrowRight className="h-5 w-5" />
                  </Button>
                </Link>

                <Link to="/dashboard">
                  <Button variant="secondary" size="xl" className="w-full sm:w-auto text-slate-800 border-slate-300">
                    Explore Demo Dashboard
                  </Button>
                </Link>
              </div>

              {/* Sub-text disclaimer */}
              <p className="text-xs text-slate-400 font-medium pt-1">
                * No typing needed. Speech recognition in Hindi, Marathi, Bengali, Tamil & 6 more languages.
              </p>
            </div>

            {/* Right Column: 3D Orb & Simulation Card */}
            <div className="lg:col-span-5 relative flex flex-col items-center">
              <HeroOrb className="w-full h-64 sm:h-80" />

              {/* Live interactive simulation card overlay */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="w-full -mt-10 relative z-20 glass-card p-5 rounded-2xl border border-slate-200 shadow-xl space-y-3"
              >
                <div className="flex items-center justify-between text-xs border-b border-slate-100 pb-2">
                  <div className="flex items-center gap-2 font-bold text-slate-800">
                    <span className="h-2.5 w-2.5 rounded-full bg-emerald-500 animate-ping" />
                    <span>Voice Interview Simulation</span>
                  </div>
                  <DemoDataBadge text="Simulated Hindi Stream" className="text-[10px] py-0 px-1.5" />
                </div>

                <div className="space-y-2 text-xs">
                  <div className="p-2.5 rounded-xl bg-brand-50 border border-brand-100 text-brand-900 font-medium">
                    AI: &quot;नमस्ते राजेश जी, आप पहले किस प्रकार का काम करते रहे हैं?&quot;
                  </div>
                  <div className="p-2.5 rounded-xl bg-slate-900 text-white font-medium flex items-center justify-between">
                    <span>User: &quot;मैं २ साल से कृषि पंप मरम्मत और बिजली का काम करता हूँ।&quot;</span>
                    <Mic className="h-4 w-4 text-saffron-400 animate-pulse shrink-0 ml-2" />
                  </div>
                </div>

                <VoiceWaveform active={true} bars={20} height={32} colorClass="bg-brand-500" />
              </motion.div>
            </div>
          </div>
        </div>
      </section>

      {/* TRUST STRIP */}
      <section className="bg-slate-900 text-white py-8 shadow-inner">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {trustBadges.map((item, i) => {
              const Icon = item.icon;
              return (
                <div key={i} className="flex items-center gap-3">
                  <div className="p-2.5 rounded-xl bg-brand-800/60 text-saffron-400 shrink-0">
                    <Icon className="h-5 w-5" />
                  </div>
                  <span className="text-xs sm:text-sm font-bold tracking-wide">{item.title}</span>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-12 space-y-2">
          <Badge variant="default" className="text-xs">
            Simple 4-Step Journey
          </Badge>
          <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">
            How Jeevika Saarthi AI Works
          </h2>
          <p className="text-sm text-slate-600">
            From natural voice conversation to accredited NSQF certification and livelihood placement.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {steps.map((step, idx) => (
            <Card key={idx} hoverEffect className="relative flex flex-col justify-between border-slate-200">
              <div>
                <div className="text-3xl font-extrabold text-brand-600/30 mb-2">{step.num}</div>
                <h3 className="text-lg font-bold text-slate-900 mb-2">{step.title}</h3>
                <p className="text-xs text-slate-600 leading-relaxed">{step.desc}</p>
              </div>
            </Card>
          ))}
        </div>
      </section>

      {/* SAMPLE PATHWAY CARDS */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
          <div>
            <Badge variant="saffron" className="text-xs mb-2">
              Demonstration Pathways
            </Badge>
            <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">
              Sample NSQF Livelihood Pathways
            </h2>
            <p className="text-sm text-slate-600 mt-1">
              Aligned with PM-AJAY GIA micro-enterprise grants and PMKVY skill batches.
            </p>
          </div>
          <Link to="/recommendations">
            <Button variant="outline" size="sm" className="gap-2">
              <span>View All 3 Demo Pathways</span>
              <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {samplePathways.map((pathway) => (
            <Card key={pathway.id} hoverEffect className="flex flex-col justify-between border-slate-200 bg-white">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <Badge variant="default" className="text-xs">{pathway.nsqf}</Badge>
                  <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                    {pathway.fitScore}% Fit
                  </span>
                </div>
                <h3 className="text-lg font-bold text-slate-900">{pathway.title}</h3>
                <p className="text-xs text-slate-500 font-medium">{pathway.sector}</p>
                <p className="text-xs text-slate-600 leading-relaxed">{pathway.desc}</p>
                <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                  <span>Duration: <strong>{pathway.journeyTime}</strong></span>
                  <span className="text-brand-700 font-semibold">{pathway.fitBadge}</span>
                </div>
              </div>
              <div className="pt-4 mt-4 border-t border-slate-100">
                <Link to={`/pathway/${pathway.id}`}>
                  <Button variant="secondary" size="sm" className="w-full justify-between text-xs">
                    <span>Explore Pathway</span>
                    <ArrowRight className="h-3.5 w-3.5" />
                  </Button>
                </Link>
              </div>
            </Card>
          ))}
        </div>
      </section>

      {/* ACCESSIBILITY & MULTI-CHANNEL (Planned Phase 4 features clearly marked) */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="p-8 rounded-3xl bg-slate-900 text-white shadow-2xl relative overflow-hidden">
          <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            <div className="lg:col-span-7 space-y-4">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800 text-saffron-400 text-xs font-semibold">
                <Radio className="h-3.5 w-3.5 text-saffron-400" />
                <span>Multi-Channel Accessibility Vision (Phase 4 Roadmap)</span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-white">
                Designed for Low-Literacy & Rural Connectivity
              </h2>
              <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                Future phases will extend this web platform to toll-free IVR phone lines, WhatsApp voice note processing, offline field-worker kiosks, and low-bandwidth PWA sync.
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
                <div className="p-3 rounded-xl bg-slate-800/80 border border-slate-700 text-xs">
                  <PhoneCall className="h-5 w-5 text-saffron-400 mb-2" />
                  <div className="font-bold text-white">Toll-Free IVR Phone</div>
                  <div className="text-[11px] text-slate-400 mt-0.5">Feature phone voice interview</div>
                </div>

                <div className="p-3 rounded-xl bg-slate-800/80 border border-slate-700 text-xs">
                  <MessageSquare className="h-5 w-5 text-emerald-400 mb-2" />
                  <div className="font-bold text-white">WhatsApp Voice Notes</div>
                  <div className="text-[11px] text-slate-400 mt-0.5">Async voice message parsing</div>
                </div>

                <div className="p-3 rounded-xl bg-slate-800/80 border border-slate-700 text-xs">
                  <WifiOff className="h-5 w-5 text-brand-400 mb-2" />
                  <div className="font-bold text-white">Offline Kiosk Sync</div>
                  <div className="text-[11px] text-slate-400 mt-0.5">VLE offline local storage</div>
                </div>
              </div>
            </div>

            <div className="lg:col-span-5 flex justify-center">
              <div className="p-6 rounded-2xl bg-slate-800/90 border border-slate-700 text-xs space-y-3 w-full max-w-sm">
                <div className="font-bold text-white text-sm">PWA Install Status</div>
                <div className="flex items-center justify-between text-slate-300">
                  <span>Offline Service Worker:</span>
                  <span className="text-emerald-400 font-bold">Active</span>
                </div>
                <div className="flex items-center justify-between text-slate-300">
                  <span>Localstorage Profile Sync:</span>
                  <span className="text-emerald-400 font-bold">Enabled</span>
                </div>
                <div className="flex items-center justify-between text-slate-300">
                  <span>Target Platform:</span>
                  <span className="text-saffron-400 font-bold">Web (Phase 1)</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t border-slate-200 pt-8 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="font-bold text-slate-800">Jeevika Saarthi AI</span>
            <span>•</span>
            <DemoDataBadge text="Phase 1 Localhost Build" className="py-0 px-2 text-[10px]" />
          </div>
          <div className="flex items-center gap-4 text-slate-600">
            <Link to="/onboarding" className="hover:text-brand-700">Onboarding</Link>
            <Link to="/conversation" className="hover:text-brand-700">Interview</Link>
            <Link to="/recommendations" className="hover:text-brand-700">Recommendations</Link>
            <Link to="/facilitator" className="hover:text-brand-700">Facilitator</Link>
            <Link to="/admin" className="hover:text-brand-700">District Admin</Link>
          </div>
        </div>
      </footer>
    </div>
  );
};
