import PropTypes from 'prop-types';
import React from 'react';
import { useSelector } from 'react-redux';
import { VisibilityFilters } from '../actions';


const VideoPostList = () => {
    const channel = useSelector(state => state.visibilityFilter.channel);
    const videoPosts = useSelector(state => state.videoPostsByChannel.items);

    return (
        <div>
            <h3>{channel === VisibilityFilters.SELECT_ALL ? "All Posts" : channel}</h3>

            {videoPosts.map(videoPost =>
                <li className="nav-item" key={videoPost.id}>
                    {videoPost.title}
                </li>)
            }
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