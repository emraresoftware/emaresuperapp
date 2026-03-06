import { View, Text, TextInput, TouchableOpacity, KeyboardAvoidingView, Platform, StatusBar } from 'react-native'
import { useState } from 'react'
import { Link, useRouter } from 'expo-router'
import Constants from 'expo-constants'

export default function LoginScreen() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const API_URL = Constants.expoConfig?.extra?.apiUrl || 'http://localhost:8080'

  async function handleLogin() {
    if (!email || !password) { setError('E-posta ve şifre gerekli'); return }
    setLoading(true); setError('')
    try {
      const res = await fetch(`${API_URL}/api/v1/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })
      if (!res.ok) throw new Error('E-posta veya şifre hatalı')
      router.replace('/dashboard')
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <KeyboardAvoidingView
      style={{ flex: 1, backgroundColor: '#0f172a' }}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <StatusBar barStyle="light-content" backgroundColor="#0f172a" />
      <View style={{ flex: 1, justifyContent: 'center', paddingHorizontal: 24 }}>
        {/* Logo */}
        <View style={{ alignItems: 'center', marginBottom: 40 }}>
          <Text style={{ fontSize: 48 }}>⚡</Text>
          <Text style={{ color: '#ffffff', fontSize: 26, fontWeight: '800', marginTop: 8 }}>Emare SuperApp</Text>
          <Text style={{ color: '#64748b', fontSize: 15, marginTop: 4 }}>Hesabına giriş yap</Text>
        </View>

        {/* Form */}
        <View style={{ gap: 14 }}>
          <View>
            <Text style={{ color: '#94a3b8', fontSize: 13, marginBottom: 6 }}>E-posta</Text>
            <TextInput
              value={email}
              onChangeText={setEmail}
              placeholder="sen@emare.com"
              placeholderTextColor="#475569"
              keyboardType="email-address"
              autoCapitalize="none"
              style={{
                backgroundColor: '#1e293b', borderWidth: 1, borderColor: '#334155',
                borderRadius: 14, paddingHorizontal: 16, paddingVertical: 14,
                color: '#ffffff', fontSize: 15,
              }}
            />
          </View>
          <View>
            <Text style={{ color: '#94a3b8', fontSize: 13, marginBottom: 6 }}>Şifre</Text>
            <TextInput
              value={password}
              onChangeText={setPassword}
              placeholder="••••••••"
              placeholderTextColor="#475569"
              secureTextEntry
              style={{
                backgroundColor: '#1e293b', borderWidth: 1, borderColor: '#334155',
                borderRadius: 14, paddingHorizontal: 16, paddingVertical: 14,
                color: '#ffffff', fontSize: 15,
              }}
            />
          </View>

          {!!error && (
            <View style={{ backgroundColor: '#450a0a', borderRadius: 10, padding: 12, borderWidth: 1, borderColor: '#7f1d1d' }}>
              <Text style={{ color: '#fca5a5', fontSize: 13 }}>{error}</Text>
            </View>
          )}

          <TouchableOpacity
            onPress={handleLogin}
            disabled={loading}
            style={{
              backgroundColor: '#6366f1', borderRadius: 14,
              paddingVertical: 16, alignItems: 'center', marginTop: 4,
              opacity: loading ? 0.6 : 1,
            }}
          >
            <Text style={{ color: '#ffffff', fontWeight: '700', fontSize: 16 }}>
              {loading ? 'Giriş yapılıyor...' : 'Giriş Yap'}
            </Text>
          </TouchableOpacity>
        </View>

        <Text style={{ color: '#475569', fontSize: 14, textAlign: 'center', marginTop: 24 }}>
          Hesabın yok mu?{' '}
          <Link href="/register">
            <Text style={{ color: '#818cf8' }}>Kayıt ol</Text>
          </Link>
        </Text>
      </View>
    </KeyboardAvoidingView>
  )
}
