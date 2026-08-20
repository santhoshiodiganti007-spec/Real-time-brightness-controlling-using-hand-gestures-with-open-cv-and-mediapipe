import React from 'react';
import SettingsPanel from '../components/SettingsPanel';

export default function Settings({ settings, onSaveSettings }) {
  return (
    <div className="py-4">
      <SettingsPanel settings={settings} onSaveSettings={onSaveSettings} />
    </div>
  );
}
