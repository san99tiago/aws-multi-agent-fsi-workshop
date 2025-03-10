const CopyWebpackPlugin = require('copy-webpack-plugin');
const webpack = require('webpack');
const path = require('path');

module.exports = {
  mode: 'development',
  entry: './src/app.js',
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'dist')
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        generator: {
          filename: 'js/[name][ext]'
        }
      },
      {
        test: /\.(png|jpe?g|gif|svg)$/i,
        type: 'asset/resource',
        generator: {
          filename: 'images/[name][ext]'
        }
      },
      {
        test: /\.css$/,
        type: 'asset/resource',
        generator: {
          filename: 'css/[name][ext]'
        }
      },
      {
        test: /\.ttf$/,
        type: 'asset/resource',
        generator: {
          filename: 'fonts/[name][ext]'
        }
      },

    ]
  },
  devServer: {
    client: {
      overlay: true
    },
    hot: true,
    watchFiles: ['src/*', 'index.html']
  },
  plugins: [
    new CopyWebpackPlugin({
      patterns: [
        { from: 'index.html', to: 'index.html' },
        { from: 'src/images', to: 'images' },
        { from: 'src/css', to: 'css' },
        { from: 'src/fonts', to: 'fonts' },
        //{ from: 'src/js', to: 'js' }

      ]
    }),
    new webpack.HotModuleReplacementPlugin()
  ]
};
