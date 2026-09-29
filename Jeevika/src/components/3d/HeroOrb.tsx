import React from 'react';
import { motion } from 'framer-motion';
import { useAppStore } from '../../stores/useAppStore';

export const HeroOrb: React.FC<{ className?: string }> = ({ className = '' }) => {
  const { reducedMotion } = useAppStore();

  if (reducedMotion) {
    return (
      <div className={`relative flex items-center justify-center ${className}`}>
        <div className="h-64 w-64 rounded-full bg-gradient-to-tr from-brand-700 via-brand-500 to-saffron-500 opacity-80 blur-xl" />
      </div>
    );
  }

  return (
    <div className={`relative flex items-center justify-center overflow-visible select-none ${className}`}>
      {/* Outer ambient glow */}
      <motion.div
        className="absolute h-72 w-72 sm:h-96 sm:w-96 rounded-full bg-gradient-to-tr from-brand-600/30 via-teal-400/20 to-saffron-400/30 blur-3xl"
        animate={{
          scale: [1, 1.15, 1],
          rotate: [0, 180, 360],
        }}
        transition={{
          duration: 18,
          repeat: Infinity,
          ease: 'linear',
        }}
      />

      {/* Decorative 3D Ring 1 */}
      <motion.div
        className="absolute h-64 w-64 sm:h-80 sm:w-80 rounded-full border-2 border-dashed border-brand-400/40"
        animate={{ rotate: 360 }}
        transition={{ duration: 24, repeat: Infinity, ease: 'linear' }}
      />

      {/* Decorative 3D Ring 2 */}
      <motion.div
        className="absolute h-52 w-52 sm:h-64 sm:w-64 rounded-full border border-saffron-400/50"
        animate={{ rotate: -360, scale: [0.95, 1.05, 0.95] }}
        transition={{ duration: 16, repeat: Infinity, ease: 'easeInOut' }}
      />

      {/* Core Glowing Orb */}
      <motion.div
        className="relative z-10 flex h-44 w-44 sm:h-56 sm:w-56 items-center justify-center rounded-full bg-gradient-to-br from-brand-600 via-teal-700 to-slate-900 shadow-2xl shadow-brand-700/50 ring-4 ring-white/20 backdrop-blur-md"
        animate={{
          y: [-8, 8, -8],
          boxShadow: [
            '0 20px 50px rgba(13, 148, 136, 0.3)',
            '0 30px 70px rgba(245, 158, 11, 0.4)',
            '0 20px 50px rgba(13, 148, 136, 0.3)',
          ],
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      >
        <div className="absolute inset-2 rounded-full bg-gradient-to-tr from-transparent via-white/10 to-saffron-400/20 pointer-events-none" />
        <svg className="h-20 w-20 text-white/90" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <circle cx="12" cy="12" r="9" strokeDasharray="3 3" />
          <path d="M12 2v20M2 12h20" strokeOpacity="0.4" />
          <circle cx="12" cy="12" r="3" fill="#f59e0b" />
        </svg>
      </motion.div>
    </div>
  );
};
