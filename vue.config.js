module.exports = {
  publicPath: process.env.VUE_APP_PUBLICPATH,
  devServer: {
    proxy: 'http://localhost:5042',
  },
};
