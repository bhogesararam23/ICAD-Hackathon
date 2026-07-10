import React from 'react';
import RiskBadge from './RiskBadge';

export default function AlertCard({ alert }) {
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow mb-4 border-l-4 border-gray-200">
      <div className="flex justify-between items-start mb-2">
        <RiskBadge riskLevel={alert.risk_level} />
        <span className="text-xs text-gray-500">
          {formatDate(alert.created_at)}
        </span>
      </div>
      <p className="text-sm text-gray-800">{alert.generated_message}</p>
    </div>
  );
}
