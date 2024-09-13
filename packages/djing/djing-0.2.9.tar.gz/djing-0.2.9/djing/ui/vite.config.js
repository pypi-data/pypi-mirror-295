import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  root: resolve("./src"),
  base: "/static/",
  server: {
    host: "localhost",
    port: 5173,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),
    },
    extensions: [".vue", ".js", ".jsx", ".json"],
  },
  build: {
    outDir: resolve("./dist"),
    assetsDir: "",
    manifest: true,
    emptyOutDir: true,
    target: "es2015",
    rollupOptions: {
      input: {
        main: resolve("./src/main.jsx"),
      },
      output: {
        entryFileNames: "djing/js/[name]-[hash].js",
        chunkFileNames: "djing/js/[name]-[hash].js",
        assetFileNames: "djing/[ext]/[name]-[hash].[ext]",
        compact: true,
        manualChunks: {
          vue: ["vue"],
        },
      },
    },
  },
});
