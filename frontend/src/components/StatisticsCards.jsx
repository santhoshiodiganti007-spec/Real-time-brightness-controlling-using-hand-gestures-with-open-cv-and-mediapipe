import React from 'react';
import { Clock, Activity, BarChart3, TrendingUp, TrendingDown, Eye, CheckCircle2 } from 'lucide-react';

export default function StatisticsCards({ stats, telemetry }) {
  const formatDuration = (sec) => {
    const s = Math.round(sec || 0);
    const m = Math.floor(s / 60);
    const rs = s % 60;
    return `${m}m ${rs}s`;
  };

  const cards = [
    {
      title: 'Session Duration',
      value: formatDuration(stats.session_duration_seconds),
      subtext: 'Active runtime session',
      icon: Clock,
      color: 'text-cyan-400',
      bg: 'bg-cyan-500/10'
    },
    {
      title: 'Average FPS',
      value: `${telemetry.fps || stats.average_fps || 0}`,
      subtext: 'Real-time camera frame rate',
      icon: Activity,
      color: 'text-indigo-400',
      bg: 'bg-indigo-500/10'
    },
    {
      title: 'Brightness Adjustments',
      value: stats.total_brightness_changes || 0,
      subtext: 'Hardware update events logged',
      icon: BarChart3,
      color: 'text-emerald-400',
      bg: 'bg-emerald-500/10'
    },
    {
      title: 'Average Brightness',
      value: `${Math.round(stats.average_brightness || 50)}%`,
      subtext: `Min ${Math.round(stats.min_brightness || 10)}% | Max ${Math.round(stats.max_brightness || 100)}%`,
      icon: TrendingUp,
      color: 'text-amber-400',
      bg: 'bg-amber-500/10'
    }
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((c, idx) => {
        const IconComponent = c.icon;
        return (
          <div
            key={idx}
            className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl flex items-center space-x-4 relative overflow-hidden group hover:border-slate-700 transition-all"
          >
            <div className={`p-3.5 rounded-xl ${c.bg} ${c.color} shrink-0`}>
              <IconComponent className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xs font-semibold text-slate-400">{c.title}</span>
              <div className="text-xl font-bold text-white font-mono mt-0.5">{c.value}</div>
              <span className="text-[11px] text-slate-500">{c.subtext}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
