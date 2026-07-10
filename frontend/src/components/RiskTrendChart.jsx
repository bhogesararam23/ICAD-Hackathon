import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

// Mock data for demonstration
const mockReadings = [
  { time: 'Day 1', value: 12 },
  { time: 'Day 2', value: 18 },
  { time: 'Day 3', value: 25 },
  { time: 'Day 4', value: 32 },
  { time: 'Day 5', value: 48 },
  { time: 'Day 6', value: 55 },
  { time: 'Day 7', value: 42 },
];

export default function RiskTrendChart({ hazardType, readings = mockReadings }) {
  return (
    <div className="mb-8 p-4 bg-white rounded-lg shadow">
      <h3 className="text-lg font-medium text-gray-900 mb-4">
        {hazardType.charAt(0).toUpperCase() + hazardType.slice(1)} Trend (Last 7 Days)
      </h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={readings}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="time" stroke="#6b7280" />
            <YAxis stroke="#6b7280" />
            <Tooltip
              contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '0.375rem' }}
            />
            <Line
              type="monotone"
              dataKey="value"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={{ fill: '#3b82f6', r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
