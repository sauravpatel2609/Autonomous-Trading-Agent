import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  server: {
    host: "::",
    port: 5173, // Default Vite port, will auto-increment if busy
    proxy: {
      '/predict': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/stock-data': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/portfolio': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/account': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/trades': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/agent': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/register': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/token': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/ws': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        ws: true,
      },
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  plugins: [
    react(),
    mode === 'development' &&
    componentTagger(),
  ].filter(Boolean),
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
}));
