import { useState, useEffect, useCallback } from 'react';
import wsService from '../services/websocket';
import {
  getBrightness,
  setBrightness as apiSetBrightness,
  startGestureControl,
  stopGestureControl,
  getSettings,
  updateSettings as apiUpdateSettings,
  getStatistics,
  getHistory
} from '../services/api';

export function useBrightness() {
  const [telemetry, setTelemetry] = useState({
    brightness: 50.0,
    distance: 0.0,
    normalized_distance: 0.0,
    hand_detected: false,
    gesture_active: false,
    gesture_state: 'NO_HAND',
    fps: 0.0,
    is_demo_mode: false,
    control_enabled: true
  });

  const [settings, setSettings] = useState({
    smoothing_factor: 0.2,
    sensitivity: 1.0,
    min_brightness: 10.0,
    max_brightness: 100.0,
    min_distance: 0.03,
    max_distance: 0.25,
    camera_index: 0,
    update_threshold: 2.0,
    gesture_control_enabled: true,
    demo_mode: false
  });

  const [stats, setStats] = useState({
    session_duration_seconds: 0,
    total_brightness_changes: 0,
    average_brightness: 50.0,
    min_brightness: 10.0,
    max_brightness: 100.0,
    gesture_detection_count: 0,
    detection_failures: 0,
    average_fps: 0.0,
    hand_detected: false,
    gesture_state: 'NO_HAND',
    is_demo_mode: false
  });

  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  // Subscribe to real-time WebSocket telemetry
  useEffect(() => {
    const unsubscribe = wsService.subscribe((data) => {
      setTelemetry(data);
    });
    return () => unsubscribe();
  }, []);

  // Fetch initial settings and history
  const fetchAllData = useCallback(async () => {
    try {
      setLoading(true);
      const [settingsRes, statsRes, historyRes] = await Promise.allSettled([
        getSettings(),
        getStatistics(),
        getHistory(30)
      ]);

      if (settingsRes.status === 'fulfilled') setSettings(settingsRes.value);
      if (statsRes.status === 'fulfilled') setStats(statsRes.value);
      if (historyRes.status === 'fulfilled') setHistory(historyRes.value.events || []);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAllData();
    const interval = setInterval(async () => {
      try {
        const [statsData, historyData] = await Promise.all([
          getStatistics(),
          getHistory(30)
        ]);
        setStats(statsData);
        setHistory(historyData.events || []);
      } catch (e) {
        // Silent background refresh catch
      }
    }, 3000);
    return () => clearInterval(interval);
  }, [fetchAllData]);

  const changeBrightness = async (val) => {
    try {
      const res = await apiSetBrightness(val);
      setTelemetry((prev) => ({ ...prev, brightness: res.brightness }));
    } catch (err) {
      console.error('Failed to change brightness:', err);
    }
  };

  const toggleGestureControl = async (enabled) => {
    try {
      if (enabled) {
        await startGestureControl();
      } else {
        await stopGestureControl();
      }
      setTelemetry((prev) => ({ ...prev, control_enabled: enabled }));
    } catch (err) {
      console.error('Failed to toggle gesture control:', err);
    }
  };

  const saveSettings = async (newSettings) => {
    try {
      const updated = await apiUpdateSettings(newSettings);
      setSettings(updated);
      setTelemetry((prev) => ({
        ...prev,
        control_enabled: updated.gesture_control_enabled,
        is_demo_mode: updated.demo_mode
      }));
    } catch (err) {
      console.error('Failed to update settings:', err);
    }
  };

  return {
    telemetry,
    settings,
    stats,
    history,
    loading,
    changeBrightness,
    toggleGestureControl,
    saveSettings,
    refreshData: fetchAllData
  };
}
