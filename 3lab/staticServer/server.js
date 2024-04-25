const express = require('express');
const app = express();

const host = 'localhost';
const port = 7000;

const dirName = '../assets';

app.use(
    '/sentences/get/:id',
    express.static(`${dirName}/assets/trees`)
);

app.listen(port, host, function () {
    console.log(`Server listens http://${host}:${port}`);
});