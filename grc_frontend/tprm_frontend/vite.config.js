import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// Plugin to add CORS headers for iframe embedding
const corsHeadersPlugin = () => {
  return {
    name: 'cors-headers',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        // Allow iframe embedding from GRC frontend
        res.setHeader('X-Frame-Options', 'SAMEORIGIN')
        res.setHeader('Content-Security-Policy', "frame-ancestors 'self' http://localhost:8080 http://localhost:8081 http://127.0.0.1:8080 http://127.0.0.1:8081;")
        res.setHeader('Access-Control-Allow-Origin', '*')
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        next()
      })
    }
  }
}

export default defineConfig({
  plugins: [
    corsHeadersPlugin(),
    vue({
      script: {
        defineModel: true,
        propsDestructure: true
      },
      template: {
        compilerOptions: {
          isCustomElement: (tag) => {
            // Allow Element Plus components and custom vendor components
            return tag.startsWith('el-') || tag.startsWith('vendor_') || tag.includes('-')
          }
        }
      }
    })
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      'vue': 'vue/dist/vue.esm-bundler.js'
    },
  },
  server: {
    port: 3000,
    host: '0.0.0.0',
    hmr: {
      overlay: true
    },
    cors: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  },
  esbuild: {
    target: 'es2020',
    jsxFactory: 'h',
    jsxFragment: 'Fragment'
  },
  define: {
    __VUE_OPTIONS_API__: true,
    __VUE_PROD_DEVTOOLS__: false,
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false,
    'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development')
  },
  build: {
    target: 'es2020',
    sourcemap: true,
    rollupOptions: {
      input: {
        main: 'index.html',
        rfp: 'index-rfp.html',
        vendor: 'index-vendor.html',
        contract: 'index-contract.html'
      },
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia'],
          ui: ['lucide-vue-next'],
          utils: ['axios']
        }
      }
    }
  },
  optimizeDeps: {
    include: [
      'vue', 
      'vue-router', 
      'pinia', 
      'lucide-vue-next', 
      'axios',
      'element-plus',
      '@element-plus/icons-vue',
      'zod'
    ],
    exclude: ['@vite/client', '@vite/env']
  },
  css: {
    preprocessorOptions: {
      css: {
        charset: false
      }
    }
  }
})