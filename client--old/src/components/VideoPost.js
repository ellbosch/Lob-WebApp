import React from 'react';

const VideoPost = ({videoPost}) => {
    return (
        <div>
            <video className="card-img-top" controls loop playsinline preload="auto">
                <source src={videoPost.mp4_url} type="video/mp4" />
            </video>
            <h5 className="card-title">{videoPost.title}</h5>
            <small className="text-muted timestamp" value={videoPost.date_posted}>{videoPost.date_posted}</small>
        </div>
    )
}

export default VideoPost;