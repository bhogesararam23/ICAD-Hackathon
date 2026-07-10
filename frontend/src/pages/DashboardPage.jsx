import React, { useState, useEffect } from 'react';
import LocationSelector from '../components/LocationSelector';
import RiskTrendChart from '../components/RiskTrendChart';
import AlertCard from '../components/AlertCard';
import { getLocations, getAlerts, triggerRefresh } from '../api/client';

const HAZARD_TYPES = ['rainfall', 'river_discharge'];

export default function DashboardPage() {
  const [locations, setLocations] = useState([]);
  const [selectedLocationId, setSelectedLocationId] = useState(null);
  const [selectedHazardType, setSelectedHazardType] = useState(HAZARD_TYPES[0]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load locations on mount
  useEffect(() => {
    async function loadLocations() {
      try {
        const data = await getLocations();
        setLocations(data);
      } catch (err) {
        setError('Failed to load locations');
      }
    }
    loadLocations();
  }, []);

  // Load alerts when location or hazard type changes
  useEffect(() => {
    if (!selectedLocationId) return;
    async function loadData() {
      try {
        setLoading(true);
        const alertsData = await getAlerts(selectedLocationId);
        setAlerts(alertsData);
      } catch (err) {
        setError('Failed to load data');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [selectedLocationId]);

  const handleRefresh = async () => {
    if (!selectedLocationId) return;
    try {
      setLoading(true);
      await triggerRefresh(selectedLocationId, selectedHazardType);
      // Reload alerts after refresh
      const alertsData = await getAlerts(selectedLocationId);
      setAlerts(alertsData);
    } catch (err) {
      setError('Failed to refresh data');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">IGAD Early Warning System</h1>

        {error && (
          <div className="mb-6 p-4 bg-red-50 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* Location and Hazard Type Selectors */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <LocationSelector
            locations={locations}
            selectedLocationId={selectedLocationId}
            onSelect={setSelectedLocationId}
          />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Hazard Type</label>
            <select
              value={selectedHazardType}
              onChange={(e) => setSelectedHazardType(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              {HAZARD_TYPES.map((type) => (
                <option key={type} value={type}>
                  {type.charAt(0).toUpperCase() + type.slice(1)}
                </option>
              ))}
            </select>
          </div>
          <div className="flex items-end">
            <button
              onClick={handleRefresh}
              disabled={loading || !selectedLocationId}
              className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Refreshing...' : 'Refresh Data'}
            </button>
          </div>
        </div>

        {/* Dashboard Content */}
        {selectedLocationId ? (
          <div>
            <RiskTrendChart hazardType={selectedHazardType} />
            <div className="mt-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">Recent Alerts</h2>
              {alerts.length > 0 ? (
                alerts.map((alert) => (
                  <AlertCard key={alert.id} alert={alert} />
                ))
              ) : (
                <p className="text-gray-500">No alerts for this location yet.</p>
              )}
            </div>
          </div>
        ) : (
          <p className="text-gray-600">Please select a location to view the dashboard.</p>
        )}
      </div>
    </div>
  );
}
