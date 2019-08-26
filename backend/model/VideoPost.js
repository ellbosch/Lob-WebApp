module.exports = (sequelize, DataTypes) => {
    const videoPost = sequelize.define('videopost', {
        title: {
            type: DataTypes.STRING,
            allowNull: false
        },
        source: {
            type: DataTypes.STRING,
            allowNull: false
        },
        league: {
            type: DataTypes.STRING,
            allowNull: false
        },
        date_posted: {
            type: DataTypes.DATE,
            allowNull: false
        },
        author: {
            type: DataTypes.STRING
        },
        reddit_score: {
            type: DataTypes.INTEGER
        },
        reddit_comments_url: {
            type: DataTypes.STRING
        },
        url: {
            type: DataTypes.STRING,
            allowNull: false
        },
        mp4_url: {
            type: DataTypes.STRING,
            allowNull: false
        },
        thumbnail_url: {
            type: DataTypes.STRING
        },
        height: {
            type: DataTypes.INTEGER,
            allowNull: false
        },
        width: {
            type: DataTypes.INTEGER,
            allowNull: false
        }
    }, {
        timestamps: false
    });
    return videoPost;
}
