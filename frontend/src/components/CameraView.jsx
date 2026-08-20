import React from 'react';
import { Camera, RefreshCw, Eye, EyeOff, Video, Sparkles } from 'lucide-react';

export default function CameraView({ telemetry }) {
  const [streamError, setStreamError] = React.useState(false);
  const host = typeof window !== 'undefined' ? window.location.hostname || '127.0.0.1' : '127.0.0.1';
  const streamUrl = `http://${host}:8000/api/camera/stream`;

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl relative overflow-hidden group">
      {/* Background glow */}
      <div className="absolute -top-20 -left-20 w-40 h-40 bg-cyan-500/10 rounded-full blur-3xl group-hover:bg-cyan-500/20 transition-all pointer-events-none" />

      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <div className="p-2 bg-slate-800 rounded-lg text-cyan-400">
            <Camera className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              Webcam Feed & Landmark Tracking
              <span className="flex h-2 w-2 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
            </h2>
            <p className="text-xs text-slate-400">MediaPipe 3D Landmark & Thumb-Index Distance Line Overlay</p>
          </div>
        </div>

        {/* Live Distance Gauge Pill */}
        <div className="bg-slate-800/90 px-3 py-1.5 rounded-lg border border-slate-700/80 flex items-center space-x-2">
          <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
          <span className="text-xs text-slate-300 font-mono">
            Dist: <span className="text-cyan-400 font-bold">{telemetry.distance ? telemetry.distance.toFixed(3) : '0.000'}</span>
          </span>
        </div>
      </div>

      {/* Stream Container */}
      <div className="relative aspect-video bg-slate-950 rounded-xl overflow-hidden border border-slate-800 flex items-center justify-center group/video shadow-inner">
        {!streamError ? (
          <img
            src={streamUrl}
            alt="MediaPipe Camera Stream"
            onError={() => setStreamError(true)}
            className="w-full h-full object-cover rounded-xl"
          />
        ) : (
          <div className="flex flex-col items-center justify-center p-8 text-center space-y-3">
            <Video className="w-12 h-12 text-slate-600 animate-pulse" />
            <div>
              <p className="text-sm font-semibold text-slate-300">Camera Stream Standby</p>
              <p className="text-xs text-slate-500 mt-1">Starting camera hardware or background service...</p>
            </div>
            <button
              onClick={() => setStreamError(false)}
              className="mt-2 flex items-center space-x-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-cyan-400 rounded-lg border border-slate-700 transition-all"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Retry Stream</span>
            </button>
          </div>
        )}

        {/* Floating Overlay HUD Badge */}
        <div className="absolute bottom-4 left-4 bg-slate-900/90 backdrop-blur-md px-3.5 py-2 rounded-lg border border-slate-700 flex items-center space-x-3 shadow-lg">
          <div className="flex items-center space-x-2">
            <div className={`w-2.5 h-2.5 rounded-full ${telemetry.hand_detected ? 'bg-emerald-400 animate-pulse' : 'bg-slate-500'}`} />
            <span className="text-xs font-semibold text-slate-200">
              {telemetry.hand_detected ? 'Hand Detected' : 'No Hand in View'}
            </span>
          </div>
          <span className="text-slate-600">|</span>
          <span className="text-xs font-mono text-cyan-400">
            {telemetry.gesture_state || 'NO_HAND'}
          </span>
        </div>

        {/* Visual Brightness HUD Bar on Right Side */}
        <div className="absolute right-4 top-4 bottom-4 w-3 bg-slate-900/80 rounded-full border border-slate-700 overflow-hidden flex flex-col justify-end">
          <div
            className="bg-gradient-to-t from-cyan-500 to-emerald-400 w-full transition-all duration-150 rounded-full"
            style={{ height: `${telemetry.brightness || 50}%` }}
          />
        </div>
      </div>
    </div>
  );
}
