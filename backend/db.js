const Sequelize = require('sequelize');
const VideoPostModel = require('./model/VideoPost');
require('dotenv').config();

// DB connection
const sequelize = new Sequelize(process.env.RDS_DB, process.env.RDS_USERNAME, process.env.RDS_PASSWORD, {
    dialect     : 'mysql',
    host        : process.env.RDS_HOSTNAME,
    port        : process.env.RDS_PORT,
    logging     : false,
    define      : {
        charset: process.env.RDS_CHARSET,
        freezeTableName: true
    }
});
sequelize
    .authenticate()
    .then(() => {
        console.log('Connection to DB has been established');
    })
    .catch(err => {
        console.error('Unable to connect to DB:', err);
    });

const VideoPost = VideoPostModel(sequelize, Sequelize);

module.exports = {
    VideoPost
}