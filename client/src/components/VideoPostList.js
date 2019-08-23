import PropTypes from 'prop-types';
import React from 'react';
import { useSelector } from 'react-redux';


const VideoPostList = () => {
    const filter = useSelector(state => state.visibilityFilter)

    return (
        <div>
            <p>Videos:</p>
            {filter}
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