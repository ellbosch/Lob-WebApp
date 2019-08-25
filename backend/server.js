const bodyParser = require('body-parser');
const express = require('express');
const fetch = require('node-fetch');
const path = require('path');
const Sequelize = require('sequelize');
require('dotenv').config();

// DB connection
const sequelize = new Sequelize( process.env.RDS_DB, process.env.RDS_USERNAME, process.env.RDS_PASSWORD, {
    dialect     : 'mysql',
    host        : process.env.RDS_HOSTNAME,
    port        : process.env.RDS_PORT,
    define      : { charset: process.env.RDS_CHARSET }
});
sequelize
    .authenticate()
    .then(() => {
        console.log('Connection to DB has been established');
    })
    .catch(err => {
        console.error('Unable to connect to DB:', err);
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