import Head from "next/head";
import Link from "next/link";
import { useState } from "react";
import { useServices, useServicesHealth } from "../hooks/useServices";
import type { ServiceStatus } from "../utils/api";

const STATUS_LABELS: Record<ServiceStatus | "all", string> = {
  all: "Tümü",
  production: "Yayında",
  ready: "Hazır",
  development: "Geliştirme",
  planning: "Planlama",
};

const STATUS_COLORS: Record<string, string> = {
  production: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
  ready: "bg-blue-500/20 text-blue-400 border-blue-500/30",
  development: "bg-amber-500/20 text-amber-400 border-amber-500/30",
  planning: "bg-slate-500/20 text-slate-400 border-slate-500/30",
};

const HEALTH_COLORS: Record<string, string> = {
  healthy: "text-emerald-400",
  offline: "text-red-400",
  timeout: "text-amber-400",
  error: "text-red-400",
  no_url: "text-slate-500",
};

export default function ServicesPage() {
  const [filter, setFilter] = useState<ServiceStatus | "all">("all");
  const { services, loading, error } = useServices(filter === "all" ? undefined : filter);
  const { results: health, summary, loading: healthLoading, check } = useServicesHealth("production");

  return (
    <>
      <Head>
        <title>Servisler — Emare SuperApp</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#6366f1" />
      </Head>

      <main className="min-h-screen bg-slate-950 pb-24">
        {/* Header */}
        <header className="px-4 pt-12 pb-6">
          <div className="flex items-center justify-between">
            <div>
              <Link href="/dashboard" className="text-slate-500 text-sm mb-1 block">← Dashboard</Link>
              <h1 className="text-2xl font-bold text-white">Emare Ekosistemi</h1>
              <p className="text-slate-400 text-sm mt-1">{services.length} servis</p>
            </div>
            <button
              onClick={check}
              disabled={healthLoading}
              className="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 text-sm hover:bg-slate-700 disabled:opacity-50"
            >
              {healthLoading ? "Kontrol…" : "🩺 Sağlık"}
            </button>
          </div>

          {/* Sağlık özeti */}
          {summary.total > 0 && (
            <div className="mt-4 flex gap-3">
              <span className="text-sm text-emerald-400 font-medium">✅ {summary.healthy} sağlıklı</span>
              {summary.offline > 0 && (
                <span className="text-sm text-red-400 font-medium">❌ {summary.offline} erişilemiyor</span>
              )}
            </div>
          )}
        </header>

        {/* Filtreler */}
        <div className="px-4 flex gap-2 overflow-x-auto pb-2 no-scrollbar">
          {(Object.keys(STATUS_LABELS) as (ServiceStatus | "all")[]).map((s) => (
            <button
              key={s}
              onClick={() => setFilter(s)}
              className={`shrink-0 px-3 py-1.5 rounded-full text-sm font-medium border transition-colors ${
                filter === s
                  ? "bg-indigo-600 text-white border-indigo-500"
                  : "bg-slate-800 text-slate-400 border-slate-700 hover:border-slate-500"
              }`}
            >
              {STATUS_LABELS[s]}
            </button>
          ))}
        </div>

        {/* Servis listesi */}
        <div className="px-4 mt-4 space-y-3">
          {loading && (
            <p className="text-slate-500 text-center py-12">Yükleniyor…</p>
          )}
          {error && (
            <p className="text-red-400 text-center py-12">Hata: {error}</p>
          )}
          {!loading && !error && services.map((svc) => {
            const h = health.find((r) => r.id === svc.id);
            return (
              <div
                key={svc.id}
                className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex items-center gap-4"
              >
                <span className="text-3xl">{svc.icon}</span>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="text-white font-semibold">{svc.name}</span>
                    <span
                      className={`text-xs px-2 py-0.5 rounded-full border ${STATUS_COLORS[svc.status] ?? STATUS_COLORS.planning}`}
                    >
                      {STATUS_LABELS[svc.status]}
                    </span>
                  </div>
                  <p className="text-slate-500 text-xs mt-0.5 truncate">{svc.url}</p>
                  <p className="text-slate-600 text-xs mt-0.5">{svc.category}</p>
                </div>
                {h && (
                  <span className={`text-xs font-bold ${HEALTH_COLORS[h.status] ?? "text-slate-500"}`}>
                    {h.reachable ? "●" : "○"}
                  </span>
                )}
              </div>
            );
          })}
        </div>
      </main>
    </>
  );
}
