const AWS = require('aws-sdk');
const bodyParser = require('body-parser');
const express = require('express');
const path = require('path');
const { VideoPost } = require('./db');

// dynamodb connection details
AWS.config.update({
    region: "us-west-2"
});
const docClient = new AWS.DynamoDB.DocumentClient();

// express configuration
const app = express();
const API_PORT = process.env.HTTP_PORT || 3001;

app.use(express.static(path.join(__dirname, '../client/build')));
app.use(bodyParser.json());

app.get('/', function(req, res) {
	res.sendFile(path.join(__dirname, '../client/build', 'index.html'));
});

// v1.1 api calls
// const getPosts1_1 = (req, res) => {
// }

// v1 api calls
const getPosts1 = (req, res) => {
    const channel = req.query.channel;
    const page = (typeof req.query.page !== 'undefined') ? parseInt(req.query.page) : 0;

    if (typeof channel !== 'undefined') {
        getVideoPostsForChannel(channel, page, (videoPosts) => res.json({ results: videoPosts }));
    } else {
        const params = {
            TableName: 'lobHotPostsByLeague'
        };

        docClient.scan(params, (err, data) => {
            if (err) {
                console.error("Unable to get item. Error JSON:", JSON.stringify(err, null, 2));
            } else {
                // flatten items into 1d sorted array
                const allItems = data["Items"]
                    .map(obj => obj.posts)
                    .reduce((prev, current) => prev.concat(current))
                    .sort((a, b) => b.hot_score - a.hot_score);

                res.json({ results: allItems });
            }
        });
    }
}

// uses sequalize to return paginated video posts
const getVideoPostsForChannel = (channel, page, success) => {
    const limit = 10;

    VideoPost.findAll({
        where: { league: channel },
        order: [ ['date_posted', 'DESC'] ],
        limit: limit,
        offset: page * limit
    }).then(videoPosts => {
        success(videoPosts);
    }).catch(error => {
        console.log(error);
    });
}

// routers for different api versions
// var v1_1 = express.Router();
var v1 = express.Router();
var v0 = express.Router();

// v1_1
// v1_1.use('/posts', express.Router()
//     .get('/', getPosts1_1)
// );

// v1
v1.use('/posts', express.Router()
    .get('/', getPosts1)
);

// v0 versioning here

// api versioning paths
// app.use('/api/v1.1', v1_1);
app.use('/api/v1', v1);
app.use('/', v0);

// launch our backend into a port
app.listen(API_PORT, () => console.log(`LISTENING ON PORT ${API_PORT}`));