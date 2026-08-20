import React from 'react';
import { Sun, Sliders, ShieldAlert, Cpu } from 'lucide-react';

export default function BrightnessMeter({ telemetry, onChangeBrightness }) {
  const currentVal = Math.round(telemetry.brightness || 50);

  // SVG Circular progress math
  const radius = 64;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (currentVal / 100) * circumference;

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between relative overflow-hidden group">
      {/* Subtle radial glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 bg-cyan-500/10 rounded-full blur-3xl group-hover:bg-cyan-500/20 transition-all pointer-events-none" />

      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <div className="p-2 bg-slate-800 rounded-lg text-amber-400">
            <Sun className="w-5 h-5 animate-spin-slow" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white">Current Screen Brightness</h2>
            <p className="text-xs text-slate-400">Real-Time Monitor Hardware Output Level</p>
          </div>
        </div>
      </div>

      {/* Main Gauge Visual */}
      <div className="flex flex-col items-center justify-center my-4 relative">
        <svg className="w-44 h-44 transform -rotate-90">
          <circle
            cx="88"
            cy="88"
            r={radius}
            className="text-slate-800"
            strokeWidth="12"
            stroke="currentColor"
            fill="transparent"
          />
          <circle
            cx="88"
            cy="88"
            r={radius}
            className="text-cyan-400 transition-all duration-300 ease-out"
            strokeWidth="12"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            stroke="currentColor"
            fill="transparent"
          />
        </svg>

        {/* Center Percentage Display */}
        <div className="absolute flex flex-col items-center justify-center text-center">
          <span className="text-4xl font-extrabold text-white tracking-tight font-mono">
            {currentVal}%
          </span>
          <span className="text-[10px] uppercase tracking-wider font-semibold text-cyan-400 mt-1">
            {telemetry.is_demo_mode ? 'Simulated Output' : 'Display Hardware'}
          </span>
        </div>
      </div>

      {/* Manual Slider & Quick Presets */}
      <div className="space-y-3 mt-2">
        <div className="flex items-center justify-between text-xs text-slate-400 font-medium">
          <span>Manual Override</span>
          <span className="text-cyan-400 font-bold">{currentVal}%</span>
        </div>
        <input
          type="range"
          min="10"
          max="100"
          value={currentVal}
          onChange={(e) => onChangeBrightness(parseFloat(e.target.value))}
          className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400"
        />

        {/* Quick Preset Buttons */}
        <div className="grid grid-cols-4 gap-2 pt-1">
          {[25, 50, 75, 100].map((preset) => (
            <button
              key={preset}
              onClick={() => onChangeBrightness(preset)}
              className={`py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                currentVal === preset
                  ? 'bg-cyan-500/20 text-cyan-400 border-cyan-500/40 shadow-sm shadow-cyan-500/20'
                  : 'bg-slate-800/80 text-slate-300 border-slate-700/80 hover:bg-slate-700/80'
              }`}
            >
              {preset}%
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
