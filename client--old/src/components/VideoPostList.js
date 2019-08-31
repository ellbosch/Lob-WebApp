import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchVideoPosts, VisibilityFilters } from '../actions';
import VideoPost from './VideoPost';

const VideoPostList = () => {
    const filter = useSelector(state => state.visibilityFilter.filter);
    const channel = useSelector(state => state.visibilityFilter.channel);
    var videoPosts = useSelector(state => state.videoPostsByChannel.items);
    const dispatch = useDispatch();

    // this is a temporary solution into pagination is introduced for blob
    if (filter === VisibilityFilters.SELECT_ALL) {
        videoPosts = videoPosts.slice(0, Math.min(10, videoPosts.length));
    }

    const fetchNextPosts = () => {
        dispatch(fetchVideoPosts(channel));
    }

    return (
        <div>
            <h3>{filter === VisibilityFilters.SELECT_ALL ? "All Posts" : channel}</h3>

            { videoPosts.map(videoPost => <VideoPost videoPost={videoPost} />) }
            <button onClick={fetchNextPosts}>MORE</button>
        </div>
    );
}

export default VideoPostList;