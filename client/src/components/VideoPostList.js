import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';


function VideoPostList({videoPosts}) {
    return (
        <div>Whatever</div>
    );
}


VideoPostList.propTypes = {
    // selectedChannel: PropTypes.string.isRequired,
    videoPosts: PropTypes.array.isRequired,
    // isFetching: PropTypes.bool.isRequired,
    // lastUpdated: PropTypes.number,
    // dispatch: PropTypes.func.isRequired
}

const mapStateToProps = state => {
//     const { selectedChannel, videoPostsByChannel } = state;
//     const {
//         isFetching,
//         lastUpdated,
//         items: videoPosts
//     } = videoPostsByChannel[selectedChannel] || {
//         isFetching: true,
//         items: []
//     }

//     return {
//         selectedChannel,
//         videoPosts,
//         isFetching,
//         lastUpdated
//     }
    return {videoPosts: []}
}

export default connect(mapStateToProps)(VideoPostList);

// export default VideoPostList;