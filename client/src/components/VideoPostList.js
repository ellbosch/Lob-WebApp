// import PropTypes from 'prop-types';
import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchVideoPosts, VisibilityFilters } from '../actions';


const VideoPostList = () => {
    // const [page, setPage] = useState(0);
    const filter = useSelector(state => state.visibilityFilter.filter);
    const channel = useSelector(state => state.visibilityFilter.channel);
    const videoPosts = useSelector(state => state.videoPostsByChannel.items);
    const dispatch = useDispatch();

    const fetchNextPosts = () => {
        // setPage(page + 1);
        // dispatch(fetchVideoPosts(channel, page));
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


// VideoPostList.propTypes = {
    // selectedChannel: PropTypes.string.isRequired,
    // videoPosts: PropTypes.array.isRequired,
    // isFetching: PropTypes.bool.isRequired,
    // lastUpdated: PropTypes.number,
    // dispatch: PropTypes.func.isRequired
// }

export default VideoPostList;