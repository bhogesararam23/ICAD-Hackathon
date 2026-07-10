const API_BASE_URL = 'http://localhost:8000';

export async function fetchApi(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });
  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }
  return response.json();
}

export async function getLocations() {
  return fetchApi('/locations');
}

export async function getLatestHazard(locationId, hazardType) {
  return fetchApi(`/locations/${locationId}/hazards/${hazardType}/latest`);
}

export async function getAlerts(locationId) {
  return fetchApi(`/locations/${locationId}/alerts`);
}

export async function triggerRefresh(locationId, hazardType) {
  return fetchApi(`/locations/${locationId}/hazards/${hazardType}/refresh`, {
    method: 'POST',
  });
}
