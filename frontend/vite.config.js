import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  base: '/static/frontend/',
  plugins: [react()],
  build: {
    outDir: '../taskorganiser/static/frontend',
    assetsDir: 'assets',
    manifest: true,
    rollupOptions: {
      input: 'index.html',
    },
  },
})
