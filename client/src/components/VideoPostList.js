import PropTypes from 'prop-types';
import React from 'react';
import { useSelector } from 'react-redux';


const VideoPostList = () => {
    const videoPosts = useSelector(state => state.items)

    return (
        <div>Whatever</div>
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