import React, { useState, useEffect } from 'react';
import { Sliders, Save, RefreshCw, Shield, Zap } from 'lucide-react';

export default function SettingsPanel({ settings, onSaveSettings }) {
  const [form, setForm] = useState(settings);
  const [savedMsg, setSavedMsg] = useState(false);

  useEffect(() => {
    setForm(settings);
  }, [settings]);

  const handleChange = (field, val) => {
    setForm((prev) => ({ ...prev, [field]: parseFloat(val) }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSaveSettings(form);
    setSavedMsg(true);
    setTimeout(() => setSavedMsg(false), 3000);
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl max-w-3xl mx-auto space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-slate-800 rounded-xl text-cyan-400">
            <Sliders className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">Application & Engine Settings</h2>
            <p className="text-xs text-slate-400">Configure Computer Vision, Signal Smoothing & Hardware Safety Bounds</p>
          </div>
        </div>

        {savedMsg && (
          <span className="text-xs px-3 py-1.5 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 font-semibold animate-fade-in">
            Settings Saved!
          </span>
        )}
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        
        {/* Signal Smoothing & Sensitivity Section */}
        <div className="space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-1.5">
            <Zap className="w-4 h-4" />
            Signal Smoothing & Sensitivity
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            {/* Smoothing Alpha */}
            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2">
              <div className="flex justify-between text-xs font-semibold text-slate-300">
                <span>Smoothing Factor (&alpha;)</span>
                <span className="text-cyan-400 font-mono">{form.smoothing_factor}</span>
              </div>
              <input
                type="range"
                min="0.05"
                max="0.8"
                step="0.05"
                value={form.smoothing_factor || 0.2}
                onChange={(e) => handleChange('smoothing_factor', e.target.value)}
                className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400"
              />
              <p className="text-[11px] text-slate-500">Lower values provide smoother output; higher values increase responsiveness.</p>
            </div>

            {/* Gesture Sensitivity */}
            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2">
              <div className="flex justify-between text-xs font-semibold text-slate-300">
                <span>Gesture Sensitivity</span>
                <span className="text-cyan-400 font-mono">{form.sensitivity}x</span>
              </div>
              <input
                type="range"
                min="0.5"
                max="2.5"
                step="0.1"
                value={form.sensitivity || 1.0}
                onChange={(e) => handleChange('sensitivity', e.target.value)}
                className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400"
              />
              <p className="text-[11px] text-slate-500">Multiplier applied to finger pinch distance normalization.</p>
            </div>

          </div>
        </div>

        {/* Hardware Safety Bounds */}
        <div className="space-y-4 pt-2">
          <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-1.5">
            <Shield className="w-4 h-4" />
            Brightness Hardware Bounds
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            {/* Min Brightness Limit */}
            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2">
              <div className="flex justify-between text-xs font-semibold text-slate-300">
                <span>Minimum Brightness Limit</span>
                <span className="text-emerald-400 font-mono">{form.min_brightness}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="50"
                step="5"
                value={form.min_brightness || 10}
                onChange={(e) => handleChange('min_brightness', e.target.value)}
                className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-400"
              />
              <p className="text-[11px] text-slate-500">Safety floor preventing screen from becoming pitch black.</p>
            </div>

            {/* Max Brightness Limit */}
            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-2">
              <div className="flex justify-between text-xs font-semibold text-slate-300">
                <span>Maximum Brightness Limit</span>
                <span className="text-emerald-400 font-mono">{form.max_brightness}%</span>
              </div>
              <input
                type="range"
                min="50"
                max="100"
                step="5"
                value={form.max_brightness || 100}
                onChange={(e) => handleChange('max_brightness', e.target.value)}
                className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-400"
              />
              <p className="text-[11px] text-slate-500">Maximum brightness threshold limit.</p>
            </div>

          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-end space-x-3 pt-4 border-t border-slate-800">
          <button
            type="submit"
            className="flex items-center space-x-2 px-6 py-2.5 bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-slate-950 font-bold text-xs rounded-xl shadow-lg shadow-cyan-500/20 transition-all"
          >
            <Save className="w-4 h-4" />
            <span>Save Configuration</span>
          </button>
        </div>

      </form>
    </div>
  );
}
