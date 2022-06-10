import express from 'express'
import fs from 'fs'
import path from 'path'
import React from 'react'
import 'ignore-styles'
import ReactDOMServer from 'react-dom/server'
import { App } from "../src/components/App/App"

const server = express();
const port = 9000;

server.get( /\.(js|css|map|ico)$/, express.static( path.resolve( __dirname, '../public' ) ) );

/*const manifest = fs.readFileSync(
    path.join(__dirname, 'static/manifest.json'),
    'utf-8'
)
const assets = JSON.parse(manifest)*/


server.get('/', (req, res) => {
    let indexHTML = fs.readFileSync(path.resolve(__dirname, '../public/index.html'), {
        encoding: 'utf8',
    });
    const component = ReactDOMServer.renderToString(React.createElement(App));
    indexHTML = indexHTML.replace( '<div id="root"></div>', `<div id="root">${ component }</div>`);
    res.contentType( 'text/html' );
    res.status( 200 );
    return res.send( indexHTML );
});

server.listen(port);

