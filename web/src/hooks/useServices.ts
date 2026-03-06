import { useState, useEffect, useCallback } from "react";
import { servicesApi, EcosystemService, HealthResult, ServiceStatus } from "../utils/api";

// ── Servis listesi hook'u ─────────────────────────────────────────────────

export function useServices(status?: ServiceStatus) {
  const [services, setServices] = useState<EcosystemService[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await servicesApi.list(status);
      setServices(data);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }, [status]);

  useEffect(() => { refresh(); }, [refresh]);

  return { services, loading, error, refresh };
}

// ── Tüm servislerin sağlık durumu hook'u ─────────────────────────────────

export function useServicesHealth(status?: ServiceStatus) {
  const [results, setResults] = useState<HealthResult[]>([]);
  const [summary, setSummary] = useState({ total: 0, healthy: 0, offline: 0 });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const check = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await servicesApi.healthAll(status);
      setResults(data.services);
      setSummary({ total: data.total, healthy: data.healthy, offline: data.offline });
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }, [status]);

  return { results, summary, loading, error, check };
}

// ── Tek servis hook'u ─────────────────────────────────────────────────────

export function useService(id: string) {
  const [service, setService] = useState<EcosystemService | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    let cancelled = false;
    setLoading(true);
    servicesApi.detail(id)
      .then((d) => { if (!cancelled) setService(d); })
      .catch((err) => { if (!cancelled) setError((err as Error).message); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [id]);

  return { service, loading, error };
}
