const path = require('path')

var HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  entry: {
    app: "./static/js/apf.js",
    vendor: "./static/js/vendor.js",
    img: "./static/img/ferrarka.jpg",
    index: "./static/js/index.js",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ["babel-loader"],
      },
      {
        test: /\.html$/,
        use: ["html-loader"]
      },
      {
        test: /\.(svg|png|jpg|gif)$/,
        use: {
          loader: "file-loader",
          options: {
            name: "[name].[hash].[ext]",
            outputPath: "./static/img"
          }
        }
      }
    ]
  },
  resolve: {
    extensions: ["*", ".js", ".jsx"],
  },
};
