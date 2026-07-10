import React from 'react';

const riskStyles = {
  low: 'bg-green-100 text-green-800',
  moderate: 'bg-yellow-100 text-yellow-800',
  high: 'bg-red-100 text-red-800',
};

export default function RiskBadge({ riskLevel }) {
  const style = riskStyles[riskLevel.toLowerCase()] || riskStyles.low;
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${style}`}>
      {riskLevel.charAt(0).toUpperCase() + riskLevel.slice(1)} Risk
    </span>
  );
}
