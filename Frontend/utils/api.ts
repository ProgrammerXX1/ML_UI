// utils/api.ts
export const API_BASE = 'http://127.0.0.1:8000';

export async function apiFetch(path: string, options: RequestInit = {}) {
  const token = localStorage.getItem('access_token');

  return await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  }).then(res => {
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return res.json();
  });
}
