import React, { useState } from 'react';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import Settings from './pages/Settings';
import About from './pages/About';
import { useBrightness } from './hooks/useBrightness';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const {
    telemetry,
    settings,
    stats,
    history,
    loading,
    changeBrightness,
    toggleGestureControl,
    saveSettings
  } = useBrightness();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-cyan-500 selection:text-slate-950">
      
      {/* Top Header */}
      <Header
        telemetry={telemetry}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      {/* Main Page Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === 'dashboard' && (
          <Dashboard
            telemetry={telemetry}
            stats={stats}
            history={history}
            onChangeBrightness={changeBrightness}
            onToggleControl={toggleGestureControl}
          />
        )}

        {activeTab === 'settings' && (
          <Settings
            settings={settings}
            onSaveSettings={saveSettings}
          />
        )}

        {activeTab === 'about' && <About />}
      </main>

      {/* Bottom Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6 mt-12 text-center text-xs text-slate-500">
        <p>Touchless Brightness Control &copy; {new Date().getFullYear()} — Production Computer Vision System</p>
      </footer>

    </div>
  );
}
