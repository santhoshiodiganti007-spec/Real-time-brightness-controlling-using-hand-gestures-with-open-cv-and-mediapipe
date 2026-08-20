import React, { useState } from 'react';
import { Sliders, CheckCircle2, ArrowRight, X, Sparkles, AlertCircle } from 'lucide-react';
import { startCalibration, recordCalibrationStep, saveCalibration } from '../services/api';

export default function CalibrationPanel({ onClose, telemetry }) {
  const [step, setStep] = useState(1);
  const [minDist, setMinDist] = useState(null);
  const [maxDist, setMaxDist] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleStart = async () => {
    try {
      setLoading(true);
      setErrorMsg(null);
      await startCalibration();
      setStep(1);
    } catch (e) {
      setErrorMsg('Failed to start calibration session.');
    } finally {
      setLoading(false);
    }
  };

  const handleRecordMin = async () => {
    try {
      setLoading(true);
      setErrorMsg(null);
      const res = await recordCalibrationStep('min');
      setMinDist(res.min_distance);
      setStep(2);
    } catch (e) {
      setErrorMsg(e.response?.data?.detail || 'No hand detected in webcam view. Hold hand in front of camera.');
    } finally {
      setLoading(false);
    }
  };

  const handleRecordMax = async () => {
    try {
      setLoading(true);
      setErrorMsg(null);
      const res = await recordCalibrationStep('max');
      setMaxDist(res.max_distance);
      setStep(3);
    } catch (e) {
      setErrorMsg(e.response?.data?.detail || 'Failed to capture maximum spread distance.');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      setLoading(true);
      setErrorMsg(null);
      await saveCalibration();
      onClose();
    } catch (e) {
      setErrorMsg(e.response?.data?.detail || 'Failed to save calibration.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-md p-4 animate-fade-in">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-lg w-full shadow-2xl relative space-y-6">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-all"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Title */}
        <div className="flex items-center space-x-3">
          <div className="p-3 bg-indigo-500/10 text-indigo-400 rounded-xl border border-indigo-500/20">
            <Sliders className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">Guided Hand Pinch Calibration</h2>
            <p className="text-xs text-slate-400">Personalize distance thresholds for your hand size</p>
          </div>
        </div>

        {errorMsg && (
          <div className="p-3 bg-rose-500/10 border border-rose-500/30 rounded-xl text-rose-400 text-xs flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        {/* Live Distance Gauge */}
        <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-center justify-between">
          <span className="text-xs text-slate-400 font-medium">Live Distance Telemetry</span>
          <span className="text-lg font-mono font-bold text-cyan-400">
            {telemetry.distance ? telemetry.distance.toFixed(4) : '0.0000'}
          </span>
        </div>

        {/* Wizard Steps Content */}
        <div className="space-y-4">
          
          {step === 1 && (
            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <span className="w-6 h-6 rounded-full bg-cyan-500 text-slate-950 text-xs flex items-center justify-center font-bold">1</span>
                Set Minimum Finger Distance
              </h3>
              <p className="text-xs text-slate-400">
                Bring your thumb and index finger tip close together (pinched state), then click "Record Minimum".
              </p>
              <button
                onClick={handleRecordMin}
                disabled={loading}
                className="w-full py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs rounded-xl shadow-lg shadow-cyan-500/20 transition-all flex items-center justify-center space-x-2"
              >
                <span>Record Minimum Distance</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          )}

          {step === 2 && (
            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <span className="w-6 h-6 rounded-full bg-indigo-500 text-white text-xs flex items-center justify-center font-bold">2</span>
                Set Maximum Finger Distance
              </h3>
              <p className="text-xs text-slate-400">
                Move your thumb and index finger far apart (spread state), then click "Record Maximum".
              </p>
              <div className="text-xs text-emerald-400 font-mono">Recorded MIN: {minDist?.toFixed(4)}</div>
              <button
                onClick={handleRecordMax}
                disabled={loading}
                className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-indigo-500/20 transition-all flex items-center justify-center space-x-2"
              >
                <span>Record Maximum Distance</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          )}

          {step === 3 && (
            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 space-y-3 text-center">
              <CheckCircle2 className="w-12 h-12 text-emerald-400 mx-auto" />
              <h3 className="text-sm font-bold text-white">Calibration Complete!</h3>
              <div className="text-xs text-slate-400 space-y-1 font-mono">
                <div>MIN Distance: <span className="text-cyan-400">{minDist?.toFixed(4)}</span></div>
                <div>MAX Distance: <span className="text-cyan-400">{maxDist?.toFixed(4)}</span></div>
              </div>
              <button
                onClick={handleSave}
                disabled={loading}
                className="w-full py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs rounded-xl shadow-lg shadow-emerald-500/20 transition-all flex items-center justify-center space-x-2"
              >
                <Sparkles className="w-4 h-4" />
                <span>Save Calibration Parameters</span>
              </button>
            </div>
          )}

        </div>

      </div>
    </div>
  );
}
