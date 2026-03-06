/**
 * Emare SuperApp — API Client
 * Tüm istekler SuperApp gateway üzerinden geçer.
 */

export const API_BASE =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

// ── Temel fetch yardımcıları ──────────────────────────────────────────────

async function request<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  const token =
    typeof window !== "undefined" ? localStorage.getItem("token") : null;

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options?.headers,
    },
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail ?? `HTTP ${res.status}`);
  }

  return res.json() as Promise<T>;
}

export const api = {
  get: <T>(path: string, init?: RequestInit) =>
    request<T>(path, { method: "GET", ...init }),

  post: <T>(path: string, body: unknown, init?: RequestInit) =>
    request<T>(path, { method: "POST", body: JSON.stringify(body), ...init }),

  put: <T>(path: string, body: unknown, init?: RequestInit) =>
    request<T>(path, { method: "PUT", body: JSON.stringify(body), ...init }),

  delete: <T>(path: string, init?: RequestInit) =>
    request<T>(path, { method: "DELETE", ...init }),
};

// ── Auth ──────────────────────────────────────────────────────────────────

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export const authApi = {
  login: (email: string, password: string) =>
    api.post<LoginResponse>("/api/v1/auth/login", { email, password }),

  register: (data: { email: string; username: string; password: string; full_name?: string }) =>
    api.post("/api/v1/auth/register", data),

  me: () => api.get("/api/v1/users/me"),
};

// ── Servis Ekosistemi ─────────────────────────────────────────────────────

export type ServiceStatus = "production" | "ready" | "development" | "planning";

export interface EcosystemService {
  id: string;
  name: string;
  icon: string;
  url: string;
  status: ServiceStatus;
  category: string;
  description?: string;
}

export interface HealthResult {
  id: string;
  name: string;
  icon: string;
  status: string;
  reachable: boolean;
  error?: string;
}

export const servicesApi = {
  list: (status?: ServiceStatus) =>
    api.get<EcosystemService[]>(
      `/api/v1/services${status ? `?status=${status}` : ""}`,
    ),

  detail: (id: string) =>
    api.get<EcosystemService>(`/api/v1/services/${id}`),

  health: (id: string) =>
    api.get<HealthResult>(`/api/v1/services/${id}/health`),

  healthAll: (status?: ServiceStatus) =>
    api.get<{ total: number; healthy: number; offline: number; services: HealthResult[] }>(
      `/api/v1/services/health/all${status ? `?status=${status}` : ""}`,
    ),

  /** Başka bir Emare servisine SuperApp gateway üzerinden proxy isteği */
  proxy: <T>(serviceId: string, path: string, method = "GET", body?: unknown) =>
    api.get<T>(`/api/v1/services/gateway/${serviceId}/${path}`),
};

// ── Cüzdan ────────────────────────────────────────────────────────────────

export const walletApi = {
  balance: () => api.get("/api/v1/wallet/balance"),
  transactions: (limit = 20) =>
    api.get(`/api/v1/wallet/transactions?limit=${limit}`),
};

// ── Bildirimler ───────────────────────────────────────────────────────────

export const notificationsApi = {
  list: (unread = false) =>
    api.get(`/api/v1/notifications${unread ? "?unread=true" : ""}`),
};
