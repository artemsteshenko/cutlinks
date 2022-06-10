const path = require('path');
const HTMLWebpackPlugin = require( 'html-webpack-plugin' );
const MiniCssExtractPlugin = require( 'mini-css-extract-plugin' );
const CopyWebpackPlugin = require('copy-webpack-plugin');

const configuration = {
    mode: ( 'development' === process.env.NODE_ENV ? 'development' : 'production' ),
    entry: "./src/index.tsx",
    output: {
        path: path.resolve(__dirname, "public"),
        filename: "bundle.js"
    },
    resolve: {
        extensions: [".ts", ".tsx", ".js", ".jsx", ".json"]
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use:  'babel-loader'
            },
            {
                test: /\.(ts|tsx)$/,
                exclude: /node_modules/,
                use:  'ts-loader'
            },
            {
                test: /\.scss$/,
                use: [ MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader' ]
            },
            {
                test: /\.css$/,
                use: [ MiniCssExtractPlugin.loader, 'css-loader'],
                exclude:  /node_modules/
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin( {
            filename: 'styles.css'
        }),
        new HTMLWebpackPlugin( {
            filename: 'index.html',
            template: path.resolve( __dirname, 'src/index.html' ),
            minify: false,
        }),
        new CopyWebpackPlugin( {
            patterns: [
                {
                    from: path.resolve( __dirname, 'src/assets' ),
                    to: path.resolve( __dirname, 'public/assets' )
                }
            ]
        })
    ],
    devtool: 'source-map',
    devServer: {
        port: "3000",
        static: ["./assets"],
        open: true,
        hot: true,
        liveReload: true
    }
}
module.exports = configuration;