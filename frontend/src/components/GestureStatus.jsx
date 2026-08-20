import React from 'react';
import { Hand, Activity, Power, Lock, PauseCircle, PlayCircle, Sliders } from 'lucide-react';

export default function GestureStatus({ telemetry, onToggleControl, onOpenCalibration }) {
  const isEnabled = telemetry.control_enabled;

  const getStateColor = (state) => {
    switch (state) {
      case 'GESTURE_ACTIVE':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'PAUSED':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      case 'CALIBRATING':
        return 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30';
      case 'HAND_DETECTED':
        return 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30';
      default:
        return 'bg-slate-800 text-slate-400 border-slate-700';
    }
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className="p-2 bg-slate-800 rounded-lg text-indigo-400">
            <Hand className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white">Gesture Interface State</h2>
            <p className="text-xs text-slate-400">Pinch Gesture Detection & Machine Telemetry</p>
          </div>
        </div>

        {/* Enable / Disable Gesture Control Toggle */}
        <button
          onClick={() => onToggleControl(!isEnabled)}
          className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-xl text-xs font-bold border transition-all ${
            isEnabled
              ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40 shadow-sm shadow-emerald-500/20'
              : 'bg-rose-500/20 text-rose-400 border-rose-500/40'
          }`}
        >
          <Power className="w-4 h-4" />
          <span>{isEnabled ? 'Gesture Active' : 'Gesture Disabled'}</span>
        </button>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-2 gap-3">
        
        {/* Hand Detection Status */}
        <div className="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80 flex flex-col justify-between">
          <span className="text-xs text-slate-400 font-medium">Hand Detection</span>
          <div className="flex items-center space-x-2 mt-2">
            <div className={`w-3 h-3 rounded-full ${telemetry.hand_detected ? 'bg-emerald-400 animate-pulse' : 'bg-slate-600'}`} />
            <span className="text-sm font-bold text-white">
              {telemetry.hand_detected ? 'Detected in Frame' : 'No Hand Found'}
            </span>
          </div>
        </div>

        {/* Gesture State Pill */}
        <div className="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80 flex flex-col justify-between">
          <span className="text-xs text-slate-400 font-medium">Gesture State</span>
          <div className="mt-2">
            <span className={`inline-block text-xs px-2.5 py-1 rounded-lg font-bold border ${getStateColor(telemetry.gesture_state)}`}>
              {telemetry.gesture_state || 'NO_HAND'}
            </span>
          </div>
        </div>

        {/* Normalized Pinch Distance */}
        <div className="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80 flex flex-col justify-between">
          <span className="text-xs text-slate-400 font-medium">Thumb-Index Pinch Distance</span>
          <span className="text-lg font-bold font-mono text-cyan-400 mt-1">
            {telemetry.distance ? telemetry.distance.toFixed(4) : '0.0000'}
          </span>
        </div>

        {/* Action Button: Guided Calibration */}
        <div className="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80 flex flex-col justify-between">
          <span className="text-xs text-slate-400 font-medium">Personal Calibration</span>
          <button
            onClick={onOpenCalibration}
            className="mt-2 flex items-center justify-center space-x-1.5 w-full py-1.5 bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 text-xs font-semibold rounded-lg border border-indigo-500/30 transition-all"
          >
            <Sliders className="w-3.5 h-3.5" />
            <span>Calibrate Bounds</span>
          </button>
        </div>

      </div>
    </div>
  );
}
