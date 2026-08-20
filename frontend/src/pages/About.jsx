import React from 'react';
import { Sun, Cpu, ShieldCheck, Code2, Layers, BookOpen } from 'lucide-react';

export default function About() {
  return (
    <div className="max-w-4xl mx-auto space-y-8 py-4">
      
      {/* Hero Section */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-8 shadow-xl text-center space-y-4 relative overflow-hidden">
        <div className="inline-flex p-3 bg-gradient-to-tr from-cyan-500 to-indigo-600 rounded-2xl shadow-lg shadow-cyan-500/20 mb-2">
          <Sun className="w-10 h-10 text-white" />
        </div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">
          Touchless Brightness Control Using Hand Gestures
        </h1>
        <p className="text-sm text-slate-400 max-w-2xl mx-auto leading-relaxed">
          A real-time computer vision system that allows users to adjust their computer screen brightness using natural hand pinching gestures (thumb-to-index finger distance) without touching physical buttons or display menus.
        </p>

        {/* Tech Stack Badges */}
        <div className="flex flex-wrap justify-center gap-2 pt-2">
          {['Python 3.11', 'OpenCV', 'MediaPipe', 'NumPy', 'FastAPI', 'React', 'Vite', 'Tailwind CSS', 'SQLite', 'SQLAlchemy'].map((badge) => (
            <span key={badge} className="px-3 py-1 bg-slate-800 text-cyan-400 text-xs font-semibold rounded-lg border border-slate-700">
              {badge}
            </span>
          ))}
        </div>
      </div>

      {/* Architecture & Pipeline Explanation */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Computer Vision Pipeline */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-3">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Cpu className="w-5 h-5 text-cyan-400" />
            Computer Vision Pipeline
          </h2>
          <ul className="text-xs text-slate-300 space-y-2 list-disc list-inside leading-relaxed">
            <li><strong className="text-cyan-300">Frame Capture:</strong> OpenCV reads live BGR frames from webcam at 30 FPS.</li>
            <li><strong className="text-cyan-300">Hand Detection:</strong> MediaPipe detects 21 3D hand landmarks in real time.</li>
            <li><strong className="text-cyan-300">Distance Metric:</strong> Calculates 2D Euclidean distance $d = \sqrt{(x_1-x_2)^2 + (y_1-y_2)^2}$ between thumb tip (#4) and index tip (#8).</li>
            <li><strong className="text-cyan-300">Normalization:</strong> Maps raw distance into $[0.0, 1.0]$ based on user calibration bounds.</li>
            <li><strong className="text-cyan-300">Noise Smoothing:</strong> Applies Exponential Moving Average (EMA) $\alpha = 0.2$ to prevent screen brightness flicker.</li>
            <li><strong className="text-cyan-300">Hardware Execution:</strong> Updates physical monitor display brightness via OS controller APIs.</li>
          </ul>
        </div>

        {/* Privacy & Safety Statement */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-3">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Privacy & Hardware Safety
          </h2>
          <div className="text-xs text-slate-300 space-y-3 leading-relaxed">
            <p>
              <strong className="text-emerald-300">100% Local Image Processing:</strong> Webcam frames are processed entirely in local computer memory. No camera feed or images are ever uploaded or transmitted externally.
            </p>
            <p>
              <strong className="text-emerald-300">Hardware Safety Bounds:</strong> Screen brightness is strictly clamped between configurable safety bounds (default $10\%$ floor to $100\%$ ceiling) to prevent screen blackout.
            </p>
            <p>
              <strong className="text-emerald-300">Emergency Override:</strong> Gesture control can be instantly toggled off from the dashboard at any time.
            </p>
          </div>
        </div>

      </div>

    </div>
  );
}
