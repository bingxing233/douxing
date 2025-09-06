// frontend/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  compiler: {
    styledComponents: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  // 添加API代理配置，解决开发环境下的跨域问题
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*'
      }
    ]
  },
  webpack: (config, { isServer }) => {
    // Add nemo_agent to webpack externals
    config.externals.push('nemo_agent');
    return config;
  }
};

module.exports = nextConfig;