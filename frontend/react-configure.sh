#!/bin/bash

lang=''
style_framework=''
no_setup=false

function check_node_version() {
  node_version=$(node --version | cut -c2-3)

  if [[ $node_version -lt 14 ]]
  then
    echo 'Your node version is not supported. Try node 14 or higher'
    exit 1
  fi
  echo "Node version: $node_version"
}

function initialize_defaults() {
  npm init
  npm i --save-dev webpack webpack-cli webpack-dev-server
  npm i --save-dev babel-loader @babel/preset-env @babel/core @babel/plugin-transform-runtime @babel/preset-react
  npm i --save-dev babel-eslint @babel/runtime @babel/cli
  npm i --save-dev eslint eslint-config-airbnb-base eslint-plugin-jest eslint-config-prettier path
  npm i react react-dom react-router react-router-dom
  npm i axios

  mkdir src
  mkdir public
  touch babel.config.js
  touch webpack.config.js
  touch ./public/index.html
  if [[ $lang == 'ts' ]]
    then
      touch ./src/index.ts
    else
      touch ./src/index.js
  fi
}

function configure_ts() {
  if [[ $lang == 'ts' ]]
  then
    npm i --save-dev typescript ts-loader @types/react @types/react-dom
    touch tsconfig.json
  fi
}

function configure_ui_framework() {
  if [[ $style_framework == 'bootstrap' ]]
  then
    npm install react-bootstrap bootstrap
  elif [[ $style_framework == 'mui' ]]
  then
    npm install @mui/material @emotion/react @emotion/styled
  fi
}

while [ -n "$1" ]
do
  case "$1" in
  -no_setup) no_setup=true ;;
  -lang) lang="$2"
  echo "Found the lang option, with parameter value $2"
  shift ;;
  -style) style_framework="$2"
  echo "Found the style option, with parameter value $2"
  shift ;;
*) echo "$1 is not an option";;
esac
shift
done

if [[ $no_setup != true ]]
then
  check_node_version
  initialize_defaults
else
  echo 'No defaults setup performed'
fi

configure_ts
configure_ui_framework



