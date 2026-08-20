import React from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { LineChart as ChartIcon, History } from 'lucide-react';

export default function BrightnessChart({ history }) {
  const chartData = (history || []).map((ev, idx) => {
    const t = ev.timestamp ? new Date(ev.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }) : `#${idx + 1}`;
    return {
      time: t,
      brightness: Math.round(ev.brightness),
      distance: ev.gesture_distance ? parseFloat(ev.gesture_distance.toFixed(3)) : 0
    };
  });

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-slate-800 rounded-xl text-cyan-400">
            <ChartIcon className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white">Brightness History Timeline</h2>
            <p className="text-xs text-slate-400">Real-Time SQLite Persisted Brightness Adjustment Events</p>
          </div>
        </div>
        <div className="flex items-center space-x-2 text-xs text-slate-400">
          <History className="w-4 h-4 text-indigo-400" />
          <span>Last {chartData.length} records</span>
        </div>
      </div>

      <div className="h-64 w-full pt-4">
        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="time" stroke="#64748b" tick={{ fontSize: 11 }} />
              <YAxis domain={[0, 100]} stroke="#64748b" tick={{ fontSize: 11 }} unit="%" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  borderColor: '#334155',
                  borderRadius: '0.75rem',
                  color: '#fff',
                  fontSize: '12px'
                }}
              />
              <Line
                type="monotone"
                dataKey="brightness"
                stroke="#06b6d4"
                strokeWidth={3}
                dot={{ fill: '#06b6d4', r: 4 }}
                activeDot={{ r: 6, fill: '#38bdf8' }}
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div className="h-full flex items-center justify-center text-slate-500 text-xs font-mono">
            No brightness adjustment events recorded yet. Pinch fingers in front of webcam to adjust screen brightness.
          </div>
        )}
      </div>
    </div>
  );
}
