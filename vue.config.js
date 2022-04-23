module.exports = {
  // publicPath: '/static',
  outputDir: 'static',
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://localhost:5042',
        changeOrigin: true,
      },
      '^/dist': {
        target: 'http://localhost:5042',
        changeOrigin: true,
      },
    },
  },
};
