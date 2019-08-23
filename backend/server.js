const bodyParser = require('body-parser');
const express = require('express');
const fetch = require('node-fetch');
const path = require('path');

const app = express();
const API_PORT = process.env.HTTP_PORT || 3001;

app.use(express.static(path.join(__dirname, '../client/build')));
app.use(bodyParser.json());

app.get('/', function(req, res) {
	res.sendFile(path.join(__dirname, '../client/build', 'index.html'));
});

// create router for video posts
var videoPostsRouter = express.Router();

// gets info on bloom filter (i.e. it's size)
videoPostsRouter.get('/', function(req, res) {
    fetch('https://lob.tv/api/v1/posts?channel=nba&page=1')
        .then(res => res.json())
        .then(json => res.send(json));
});
app.use('/video-posts', videoPostsRouter);

// launch our backend into a port
app.listen(API_PORT, () => console.log(`LISTENING ON PORT ${API_PORT}`));