/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // PWA için output standalone
  output: 'standalone',
  // Resimler için domain izinleri
  images: {
    domains: ['emare.com'],
  },
}

module.exports = nextConfig
