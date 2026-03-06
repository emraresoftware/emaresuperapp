import Head from 'next/head'
import Link from 'next/link'

const MODULES = [
  { icon: '💳', name: 'Cüzdan', desc: '₺ 0.00', href: '/wallet', color: 'from-indigo-500/10' },
  { icon: '🛒', name: 'Pazar', desc: '0 sipariş', href: '/marketplace', color: 'from-violet-500/10' },
  { icon: '💬', name: 'Sosyal', desc: '0 mesaj', href: '/social', color: 'from-blue-500/10' },
  { icon: '🤖', name: 'AI Asistan', desc: 'Hazır', href: '/ai', color: 'from-emerald-500/10' },
  { icon: '🔔', name: 'Bildirimler', desc: '0 yeni', href: '/notifications', color: 'from-amber-500/10' },
  { icon: '📊', name: 'Analitik', desc: 'Son 7 gün', href: '/analytics', color: 'from-pink-500/10' },
]

export default function Dashboard() {
  return (
    <>
      <Head>
        <title>Dashboard — Emare SuperApp</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#6366f1" />
      </Head>

      <main className="min-h-screen bg-slate-950 pb-24">
        {/* Header */}
        <header className="px-4 pt-12 pb-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Hoş geldin 👋</p>
              <h1 className="text-2xl font-bold text-white mt-1">Dashboard</h1>
            </div>
            <Link href="/profile">
              <div className="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center text-white font-bold">
                E
              </div>
            </Link>
          </div>
        </header>

        {/* Bakiye Kartı */}
        <section className="px-4 mb-6">
          <div className="bg-gradient-to-br from-indigo-600 to-violet-600 rounded-2xl p-6">
            <p className="text-indigo-200 text-sm">Toplam Bakiye</p>
            <p className="text-white text-4xl font-bold mt-1">₺ 0.00</p>
            <div className="flex gap-3 mt-4">
              <button className="flex-1 bg-white/20 hover:bg-white/30 text-white rounded-xl py-2 text-sm font-medium transition-colors">
                💸 Gönder
              </button>
              <button className="flex-1 bg-white/20 hover:bg-white/30 text-white rounded-xl py-2 text-sm font-medium transition-colors">
                ➕ Yükle
              </button>
              <button className="flex-1 bg-white/20 hover:bg-white/30 text-white rounded-xl py-2 text-sm font-medium transition-colors">
                📋 Geçmiş
              </button>
            </div>
          </div>
        </section>

        {/* Modüller */}
        <section className="px-4">
          <h2 className="text-slate-400 text-sm font-medium mb-3">Hizmetler</h2>
          <div className="grid grid-cols-2 gap-3">
            {MODULES.map((m) => (
              <Link key={m.name} href={m.href}
                className={`bg-gradient-to-br ${m.color} to-slate-900 border border-slate-800 hover:border-indigo-500/40 rounded-2xl p-4 transition-all`}>
                <span className="text-2xl block mb-3">{m.icon}</span>
                <p className="font-semibold text-white text-sm">{m.name}</p>
                <p className="text-slate-500 text-xs mt-0.5">{m.desc}</p>
              </Link>
            ))}
          </div>
        </section>
      </main>

      {/* Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 bg-slate-900/95 backdrop-blur border-t border-slate-800 px-4 py-3">
        <div className="flex justify-around max-w-sm mx-auto">
          {[
            { icon: '🏠', label: 'Ana Sayfa', href: '/dashboard', active: true },
            { icon: '🔍', label: 'Keşfet', href: '/marketplace' },
            { icon: '💬', label: 'Mesajlar', href: '/social' },
            { icon: '👤', label: 'Profil', href: '/profile' },
          ].map((item) => (
            <Link key={item.label} href={item.href}
              className={`flex flex-col items-center gap-1 ${item.active ? 'text-indigo-400' : 'text-slate-500'}`}>
              <span className="text-xl">{item.icon}</span>
              <span className="text-xs">{item.label}</span>
            </Link>
          ))}
        </div>
      </nav>
    </>
  )
}
