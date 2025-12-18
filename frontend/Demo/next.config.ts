import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  rewrites: async () => {
    return [
      {
        source: '/api/db/:path*',
        destination: 'http://localhost:5000/api/db/:path*',
      },
      {
        source: '/api/llm/:path*',
        destination: 'http://localhost:5000/api/llm/:path*',
      },
    ];
  },
};

export default nextConfig;
