import { View, Text, TouchableOpacity, ScrollView, StatusBar } from 'react-native'
import { Link } from 'expo-router'

const MODULES = [
  { icon: '💳', name: 'Cüzdan', desc: '₺ 0.00', href: '/wallet' },
  { icon: '🛒', name: 'Pazar', desc: '0 sipariş', href: '/marketplace' },
  { icon: '💬', name: 'Sosyal', desc: '0 mesaj', href: '/social' },
  { icon: '🤖', name: 'AI Asistan', desc: 'Hazır', href: '/ai' },
  { icon: '🔔', name: 'Bildirimler', desc: '0 yeni', href: '/notifications' },
  { icon: '📊', name: 'Analitik', desc: 'Son 7 gün', href: '/analytics' },
]

export default function DashboardScreen() {
  return (
    <View style={{ flex: 1, backgroundColor: '#0f172a' }}>
      <StatusBar barStyle="light-content" backgroundColor="#0f172a" />
      <ScrollView contentContainerStyle={{ paddingBottom: 100 }}>
        {/* Header */}
        <View style={{ paddingHorizontal: 20, paddingTop: 60, paddingBottom: 20 }}>
          <Text style={{ color: '#94a3b8', fontSize: 14 }}>Hoş geldin 👋</Text>
          <Text style={{ color: '#ffffff', fontSize: 28, fontWeight: '700', marginTop: 4 }}>Dashboard</Text>
        </View>

        {/* Bakiye Kartı */}
        <View style={{
          marginHorizontal: 20, marginBottom: 24,
          backgroundColor: '#6366f1', borderRadius: 20, padding: 24,
        }}>
          <Text style={{ color: '#c7d2fe', fontSize: 13 }}>Toplam Bakiye</Text>
          <Text style={{ color: '#ffffff', fontSize: 36, fontWeight: '800', marginTop: 4 }}>₺ 0.00</Text>
          <View style={{ flexDirection: 'row', gap: 10, marginTop: 16 }}>
            {['💸 Gönder', '➕ Yükle', '📋 Geçmiş'].map((btn) => (
              <TouchableOpacity key={btn} style={{
                flex: 1, backgroundColor: 'rgba(255,255,255,0.2)',
                borderRadius: 12, paddingVertical: 10, alignItems: 'center',
              }}>
                <Text style={{ color: '#ffffff', fontSize: 12, fontWeight: '600' }}>{btn}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Modüller */}
        <View style={{ paddingHorizontal: 20 }}>
          <Text style={{ color: '#64748b', fontSize: 12, fontWeight: '600', marginBottom: 12, textTransform: 'uppercase', letterSpacing: 1 }}>
            Hizmetler
          </Text>
          <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 12 }}>
            {MODULES.map((m) => (
              <Link key={m.name} href={m.href as any} asChild>
                <TouchableOpacity style={{
                  width: '47%',
                  backgroundColor: '#1e293b',
                  borderRadius: 16,
                  padding: 16,
                  borderWidth: 1,
                  borderColor: '#334155',
                }}>
                  <Text style={{ fontSize: 28 }}>{m.icon}</Text>
                  <Text style={{ color: '#ffffff', fontWeight: '600', fontSize: 14, marginTop: 12 }}>{m.name}</Text>
                  <Text style={{ color: '#64748b', fontSize: 12, marginTop: 2 }}>{m.desc}</Text>
                </TouchableOpacity>
              </Link>
            ))}
          </View>
        </View>
      </ScrollView>

      {/* Bottom Tab Bar */}
      <View style={{
        position: 'absolute', bottom: 0, left: 0, right: 0,
        backgroundColor: '#1e293b', borderTopWidth: 1, borderTopColor: '#334155',
        flexDirection: 'row', paddingBottom: 28, paddingTop: 12,
      }}>
        {[
          { icon: '🏠', label: 'Ana Sayfa', href: '/dashboard' },
          { icon: '🔍', label: 'Keşfet', href: '/marketplace' },
          { icon: '💬', label: 'Mesajlar', href: '/social' },
          { icon: '👤', label: 'Profil', href: '/profile' },
        ].map((item, i) => (
          <Link key={item.label} href={item.href as any} asChild>
            <TouchableOpacity style={{ flex: 1, alignItems: 'center', gap: 2 }}>
              <Text style={{ fontSize: 22 }}>{item.icon}</Text>
              <Text style={{ color: i === 0 ? '#818cf8' : '#475569', fontSize: 11 }}>{item.label}</Text>
            </TouchableOpacity>
          </Link>
        ))}
      </View>
    </View>
  )
}
