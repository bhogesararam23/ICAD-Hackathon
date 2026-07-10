import React from 'react';

export default function LocationSelector({ locations, selectedLocationId, onSelect }) {
  return (
    <div className="mb-6">
      <label className="block text-sm font-medium text-gray-700 mb-2">Select Location</label>
      <select
        value={selectedLocationId || ''}
        onChange={(e) => onSelect(Number(e.target.value))}
        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
      >
        <option value="" disabled>-- Choose a location --</option>
        {locations.map((loc) => (
          <option key={loc.id} value={loc.id}>
            {loc.name}, {loc.country}
          </option>
        ))}
      </select>
    </div>
  );
}
