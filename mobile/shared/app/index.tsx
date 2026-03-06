import { View, Text, TouchableOpacity, StatusBar } from 'react-native'
import { Link } from 'expo-router'

export default function IndexScreen() {
  return (
    <View style={{ flex: 1, backgroundColor: '#0f172a', justifyContent: 'center', alignItems: 'center', paddingHorizontal: 24 }}>
      <StatusBar barStyle="light-content" backgroundColor="#0f172a" />

      <Text style={{ fontSize: 56 }}>⚡</Text>
      <Text style={{ color: '#ffffff', fontSize: 30, fontWeight: '800', marginTop: 16, textAlign: 'center' }}>
        Emare SuperApp
      </Text>
      <Text style={{ color: '#64748b', fontSize: 16, textAlign: 'center', marginTop: 10, lineHeight: 24 }}>
        Finans, bulut, AI, güvenlik{'\n'}hepsi cebinde
      </Text>

      <View style={{ marginTop: 40, gap: 12, width: '100%' }}>
        <Link href="/login" asChild>
          <TouchableOpacity style={{
            backgroundColor: '#6366f1', borderRadius: 16,
            paddingVertical: 18, alignItems: 'center',
          }}>
            <Text style={{ color: '#ffffff', fontWeight: '700', fontSize: 17 }}>Giriş Yap</Text>
          </TouchableOpacity>
        </Link>
        <Link href="/register" asChild>
          <TouchableOpacity style={{
            borderWidth: 1, borderColor: '#334155',
            borderRadius: 16, paddingVertical: 18, alignItems: 'center',
          }}>
            <Text style={{ color: '#94a3b8', fontWeight: '600', fontSize: 17 }}>Kayıt Ol</Text>
          </TouchableOpacity>
        </Link>
      </View>

      <Text style={{ color: '#1e293b', fontSize: 12, marginTop: 40 }}>Emare Ekosistemi — 2026</Text>
    </View>
  )
}
