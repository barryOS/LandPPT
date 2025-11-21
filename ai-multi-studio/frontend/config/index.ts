import { defineConfig } from '@tarojs/cli'

export default defineConfig({
  projectName: 'ai-multi-studio',
  date: '2025-11-21',
  designWidth: 750,
  deviceRatio: {
    640: 2.34 / 2,
    750: 1,
    828: 1.81 / 2
  },
  sourceRoot: 'src',
  outputRoot: 'dist',
  plugins: [],
  defineConstants: {},
  copy: {
    patterns: [],
    options: {}
  },
  framework: 'react',
  compiler: {
    type: 'webpack5'
  },
  mini: {
    postcss: {
      pxtransform: {
        enable: true
      },
      url: {
        enable: true,
        limit: 1024
      },
      cssModules: {
        enable: false
      }
    }
  },
  h5: {
    publicPath: '/',
    staticDirectory: 'static',
    devServer: {
      host: '0.0.0.0',
      port: 10086,
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true
        }
      }
    }
  }
})
