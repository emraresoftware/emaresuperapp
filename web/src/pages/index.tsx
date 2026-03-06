import Head from 'next/head'
import Link from 'next/link'

const MODULES = [
  { icon: '🔐', name: 'Auth & SSO', desc: 'Tek oturum, 2FA, biyometrik', href: '/login' },
  { icon: '💳', name: 'Cüzdan', desc: 'Dijital ödeme, kripto', href: '/wallet' },
  { icon: '🛒', name: 'Pazar', desc: 'Emare ürün & hizmetleri', href: '/marketplace' },
  { icon: '💬', name: 'Sosyal', desc: 'Mesajlaşma, feed, ekip', href: '/social' },
  { icon: '🤖', name: 'AI Asistan', desc: 'Akıllı asistan, Emare AI', href: '/ai' },
  { icon: '🔔', name: 'Bildirimler', desc: 'Push, email, SMS', href: '/notifications' },
  { icon: '📊', name: 'Analitik', desc: 'Kullanım dashboard', href: '/analytics' },
]

export default function Home() {
  return (
    <>
      <Head>
        <title>Emare SuperApp</title>
        <meta name="description" content="Tüm Emare hizmetleri tek çatı altında" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#6366f1" />
        <link rel="manifest" href="/manifest.json" />
        <link rel="apple-touch-icon" href="/icons/icon-192.png" />
      </Head>

      <main className="min-h-screen bg-slate-950">
        {/* Header */}
        <header className="border-b border-slate-800 px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl">⚡</span>
            <span className="font-bold text-xl text-white">Emare SuperApp</span>
          </div>
          <Link href="/login"
            className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
            Giriş Yap
          </Link>
        </header>

        {/* Hero */}
        <section className="text-center px-4 py-16">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Tüm Emare hizmetleri<br />
            <span className="text-indigo-400">tek bir yerden</span>
          </h1>
          <p className="text-slate-400 text-lg mb-8 max-w-md mx-auto">
            Finans, bulut, iletişim, yapay zeka, güvenlik — hepsi cebinizde.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Link href="/login"
              className="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-3 rounded-xl font-semibold transition-colors">
              Hemen Başla
            </Link>
            <Link href="/dashboard"
              className="border border-slate-700 hover:border-indigo-500 text-slate-300 px-6 py-3 rounded-xl font-semibold transition-colors">
              Demo Gör
            </Link>
          </div>
        </section>

        {/* Modules Grid */}
        <section className="px-4 pb-16 max-w-2xl mx-auto">
          <h2 className="text-slate-400 text-sm font-medium uppercase tracking-wider mb-4 text-center">Modüller</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {MODULES.map((m) => (
              <Link key={m.name} href={m.href}
                className="bg-slate-900 border border-slate-800 hover:border-indigo-500/50 rounded-xl p-4 transition-all group">
                <span className="text-2xl block mb-2">{m.icon}</span>
                <p className="font-semibold text-white text-sm group-hover:text-indigo-400 transition-colors">{m.name}</p>
                <p className="text-slate-500 text-xs mt-1">{m.desc}</p>
              </Link>
            ))}
          </div>
        </section>

        {/* PWA Install Banner */}
        <div className="fixed bottom-4 left-4 right-4 mx-auto max-w-sm">
          <div className="bg-indigo-600/20 border border-indigo-500/30 rounded-xl p-3 flex items-center gap-3 text-sm">
            <span className="text-xl">📱</span>
            <div>
              <p className="text-white font-medium">Ana Ekrana Ekle</p>
              <p className="text-indigo-300 text-xs">Uygulama gibi çalışır</p>
            </div>
          </div>
        </div>
      </main>
    </>
  )
}
