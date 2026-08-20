import React, { useState } from 'react';
import CameraView from '../components/CameraView';
import BrightnessMeter from '../components/BrightnessMeter';
import GestureStatus from '../components/GestureStatus';
import StatisticsCards from '../components/StatisticsCards';
import BrightnessChart from '../components/BrightnessChart';
import CalibrationPanel from '../components/CalibrationPanel';

export default function Dashboard({ telemetry, stats, history, onChangeBrightness, onToggleControl }) {
  const [showCalibrationModal, setShowCalibrationModal] = useState(false);

  return (
    <div className="space-y-6">
      {/* Statistics Cards Top Row */}
      <StatisticsCards stats={stats} telemetry={telemetry} />

      {/* Main Grid Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column: Camera Stream View (Spans 2 columns) */}
        <div className="lg:col-span-2 space-y-6">
          <CameraView telemetry={telemetry} />
          <GestureStatus
            telemetry={telemetry}
            onToggleControl={onToggleControl}
            onOpenCalibration={() => setShowCalibrationModal(true)}
          />
        </div>

        {/* Right Column: Brightness Meter & Controls */}
        <div className="space-y-6">
          <BrightnessMeter telemetry={telemetry} onChangeBrightness={onChangeBrightness} />
        </div>

      </div>

      {/* Historical Brightness Timeline Line Chart */}
      <BrightnessChart history={history} />

      {/* Calibration Modal */}
      {showCalibrationModal && (
        <CalibrationPanel
          telemetry={telemetry}
          onClose={() => setShowCalibrationModal(false)}
        />
      )}
    </div>
  );
}
