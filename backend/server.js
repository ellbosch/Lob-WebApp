const bodyParser = require('body-parser');
const express = require('express');
const fetch = require('node-fetch');
const path = require('path');
const { VideoPost } = require('./db');

VideoPost.findAll().then(posts => {
   console.log(posts);
})

// express configuration
const app = express();
const API_PORT = process.env.HTTP_PORT || 3001;

app.use(express.static(path.join(__dirname, '../client/build')));
app.use(bodyParser.json());

app.get('/', function(req, res) {
	res.sendFile(path.join(__dirname, '../client/build', 'index.html'));
});

// v1 api calls
const getPosts1 = (req, res) => {
    const channel = req.query.channel;
    const apiPath = (typeof channel !== 'undefined') ? 'https://lob.tv/api/v1/posts?page=1&channel=' + channel : 'https://lob.tv/api/v1/posts?page=1&sort=trending';

    fetch(apiPath)
    .then(res => res.json())
    .then(json => res.send(json));
}

// routers for different api versions
var v0 = express.Router();
var v1 = express.Router();

// v0 versioning here


// v1
v1.use('/posts', express.Router()
    .get('/', getPosts1)
);

// api versioning paths
app.use('/', v0);
app.use('/api/v1', v1);

// launch our backend into a port
app.listen(API_PORT, () => console.log(`LISTENING ON PORT ${API_PORT}`));