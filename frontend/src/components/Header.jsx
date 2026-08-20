import React from 'react';
import { Sun, Camera, ShieldCheck, Activity, Laptop, Play, Square, Settings as SettingsIcon, Info, Home } from 'lucide-react';
import { startCamera, stopCamera } from '../services/api';

export default function Header({ telemetry, activeTab, setActiveTab }) {
  const [cameraActive, setCameraActive] = React.useState(true);

  const handleStartCam = async () => {
    await startCamera(0);
    setCameraActive(true);
  };

  const handleStopCam = async () => {
    await stopCamera();
    setCameraActive(false);
  };

  return (
    <header className="bg-slate-900/80 backdrop-blur-md border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        
        {/* Title and Branding */}
        <div className="flex items-center space-x-3">
          <div className="p-3 bg-gradient-to-tr from-cyan-500 to-indigo-600 rounded-xl shadow-lg shadow-cyan-500/20">
            <Sun className="w-7 h-7 text-white animate-pulse" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white tracking-wide flex items-center gap-2">
              Touchless Brightness Control
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                v1.0 AI Edition
              </span>
            </h1>
            <p className="text-xs text-slate-400 font-medium">
              Real-Time MediaPipe Hand Gesture Recognition & OS Brightness Controller
            </p>
          </div>
        </div>

        {/* Status Indicators & Navigation */}
        <div className="flex items-center space-x-6">
          
          {/* Mode Pill */}
          <div className="flex items-center space-x-2 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
            <Laptop className="w-4 h-4 text-cyan-400" />
            <span className="text-xs text-slate-300 font-medium">
              {telemetry.is_demo_mode ? (
                <span className="text-amber-400 font-semibold">DEMO / SIMULATION MODE</span>
              ) : (
                <span className="text-emerald-400 font-semibold">LOCAL HARDWARE MODE</span>
              )}
            </span>
          </div>

          {/* FPS Counter */}
          <div className="hidden md:flex items-center space-x-2 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
            <Activity className="w-4 h-4 text-indigo-400" />
            <span className="text-xs text-slate-300 font-mono">
              FPS: <span className="text-indigo-300 font-bold">{telemetry.fps || 0}</span>
            </span>
          </div>

          {/* Camera Controls */}
          <div className="flex items-center space-x-2">
            <button
              onClick={handleStartCam}
              className="flex items-center space-x-1 px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600/20 text-emerald-400 hover:bg-emerald-600/30 border border-emerald-500/30 transition-all"
            >
              <Play className="w-3.5 h-3.5" />
              <span>Start</span>
            </button>
            <button
              onClick={handleStopCam}
              className="flex items-center space-x-1 px-3 py-1.5 text-xs font-semibold rounded-lg bg-rose-600/20 text-rose-400 hover:bg-rose-600/30 border border-rose-500/30 transition-all"
            >
              <Square className="w-3.5 h-3.5" />
              <span>Stop</span>
            </button>
          </div>

          {/* Page Tabs */}
          <nav className="flex items-center space-x-1 bg-slate-800/50 p-1 rounded-xl border border-slate-800">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'dashboard'
                  ? 'bg-cyan-500 text-slate-950 shadow-md shadow-cyan-500/20'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Home className="w-3.5 h-3.5" />
              <span>Dashboard</span>
            </button>
            <button
              onClick={() => setActiveTab('settings')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'settings'
                  ? 'bg-cyan-500 text-slate-950 shadow-md shadow-cyan-500/20'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <SettingsIcon className="w-3.5 h-3.5" />
              <span>Settings</span>
            </button>
            <button
              onClick={() => setActiveTab('about')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'about'
                  ? 'bg-cyan-500 text-slate-950 shadow-md shadow-cyan-500/20'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Info className="w-3.5 h-3.5" />
              <span>About</span>
            </button>
          </nav>
        </div>

      </div>
    </header>
  );
}
