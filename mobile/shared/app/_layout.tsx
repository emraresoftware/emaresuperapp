import { Stack } from 'expo-router'

export default function RootLayout() {
  return (
    <Stack
      screenOptions={{
        headerShown: false,
        contentStyle: { backgroundColor: '#0f172a' },
      }}
    >
      <Stack.Screen name="index" />
      <Stack.Screen name="login" />
      <Stack.Screen name="dashboard" />
      <Stack.Screen name="wallet" />
      <Stack.Screen name="marketplace" />
      <Stack.Screen name="social" />
      <Stack.Screen name="ai" />
      <Stack.Screen name="notifications" />
      <Stack.Screen name="analytics" />
      <Stack.Screen name="profile" />
    </Stack>
  )
}
