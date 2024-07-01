const { defineConfig } = require('@vue/cli-service');
const { DefinePlugin } = require('webpack');

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    plugins: [
      new DefinePlugin({
        '__VUE_OPTIONS_API__': JSON.stringify(true),
        '__VUE_PROD_DEVTOOLS__': JSON.stringify(false),
      }),
    ],
  },
});
