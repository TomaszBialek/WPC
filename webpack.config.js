const path = require('path');

module.exports = {
  entry: './api-ui/src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'main.js',
  },
};