import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'build',
    manifest: true,
  },
  server: {
    proxy: {
      '/djangoapp': 'http://localhost:8000',
    }
  }
})
