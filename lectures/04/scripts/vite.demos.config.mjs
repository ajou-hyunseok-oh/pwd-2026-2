import { defineConfig } from 'vite';
import { fileURLToPath } from 'node:url';
export default defineConfig({
  define: { 'process.env.NODE_ENV': JSON.stringify('production') },
  build: {
    outDir: fileURLToPath(new URL('../assets', import.meta.url)),
    emptyOutDir: false,
    lib: {
      entry: fileURLToPath(new URL('./react-demos.jsx', import.meta.url)),
      name: 'Week4ReactDemos',
      formats: ['iife'],
      fileName: () => 'react-demos.js',
    },
  },
});
