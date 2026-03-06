/**
 * Emare SuperApp — Mobile API Hookları
 * React Native / Expo ortamı
 */
import { useState, useEffect, useCallback } from "react";
import Constants from "expo-constants";

// Expo Constants'tan al (app.json extra.apiUrl veya env değişkeni)
export const API_BASE: string =
  (process.env.EXPO_PUBLIC_API_URL as string) ??
  (Constants.expoConfig?.extra?.apiUrl as string) ??
  "http://localhost:8000";

// ── Temel fetch ───────────────────────────────────────────────────────────

async function request<T>(
  path: string,
  token?: string | null,
  options?: RequestInit,
): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options?.headers,
    },
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? `HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

// ── Genel API hook'u ──────────────────────────────────────────────────────

export function useApi<T>(path: string, token?: string | null) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await request<T>(path, token);
      setData(result);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }, [path, token]);

  useEffect(() => { refresh(); }, [refresh]);

  return { data, loading, error, refresh };
}

// ── Auth ──────────────────────────────────────────────────────────────────

export async function login(email: string, password: string) {
  return request<{ access_token: string; token_type: string }>(
    "/api/v1/auth/login",
    null,
    { method: "POST", body: JSON.stringify({ email, password }) },
  );
}

export async function register(data: {
  email: string;
  username: string;
  password: string;
  full_name?: string;
}) {
  return request("/api/v1/auth/register", null, {
    method: "POST",
    body: JSON.stringify(data),
  });
}

// ── Servisler ─────────────────────────────────────────────────────────────

export type ServiceStatus = "production" | "ready" | "development" | "planning";

export interface EcosystemService {
  id: string;
  name: string;
  icon: string;
  url: string;
  status: ServiceStatus;
  category: string;
}

export function useServices(token?: string | null, status?: ServiceStatus) {
  const path = `/api/v1/services${status ? `?status=${status}` : ""}`;
  return useApi<EcosystemService[]>(path, token);
}

export function useServicesHealthAll(token?: string | null, status?: ServiceStatus) {
  const path = `/api/v1/services/health/all${status ? `?status=${status}` : ""}`;
  return useApi<{ total: number; healthy: number; offline: number }>(path, token);
}

// ── Cüzdan ────────────────────────────────────────────────────────────────

export function useWallet(token: string) {
  return useApi<{ balance: number; currency: string }>("/api/v1/wallet/balance", token);
}

// ── Bildirimler ───────────────────────────────────────────────────────────

export function useNotifications(token: string, unread = false) {
  return useApi<unknown[]>(
    `/api/v1/notifications${unread ? "?unread=true" : ""}`,
    token,
  );
}
