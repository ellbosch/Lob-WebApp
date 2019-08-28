import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchVideoPosts, VisibilityFilters } from '../actions';

const VideoPostList = () => {
    const filter = useSelector(state => state.visibilityFilter.filter);
    const channel = useSelector(state => state.visibilityFilter.channel);
    const videoPosts = useSelector(state => state.videoPostsByChannel.items);
    const dispatch = useDispatch();

    const fetchNextPosts = () => {
        dispatch(fetchVideoPosts(channel));
    }

    return (
        <div>
            <h3>{filter === VisibilityFilters.SELECT_ALL ? "All Posts" : channel}</h3>

            {videoPosts.map(videoPost =>
                <li className="nav-item" key={videoPost.id}>
                    {videoPost.title}
                </li>)
            }
            <button onClick={fetchNextPosts}>MORE</button>
        </div>
    );
}

export default VideoPostList;