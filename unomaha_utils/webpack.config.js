var debug = true;
var webpack = require('webpack');

module.exports = {
    context: __dirname,
    devtool: debug ? "inline-sourcemap" : null,
    entry: "./static/js/main.js",
    output: {
        path: __dirname + "/static/dist",
        filename: "main.min.js"
    },
    module: {
        loaders: [
            {test: /\.css$/, loader: 'style-loader!css-loader'},
            {test: /jquery/, loader: 'expose?$!expose?jQuery'},
            {test: /\.(woff|woff2)(\?v=\d+\.\d+\.\d+)?$/, loader: 'null-loader'},
            {test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, loader: 'null-loader'},
            {test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, loader: 'null-loader'},
            {test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, loader: 'null-loader'}
        ]
    },
    plugins: debug ? [] : [
        new webpack.optimize.DedupePlugin(),
        new webpack.optimize.OccurenceOrderPlugin(),
        new webpack.optimize.UglifyJsPlugin({ mangle: false, sourcemap: false }),
    ]
};
