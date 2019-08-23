import React, { useEffect } from 'react';
import { connect } from 'react-redux'
import { fetchVideoPosts } from '../actions'
import ChannelNav from '../components/ChannelNav';
import VideoPostList from '../components/VideoPostList';

const App = ({ dispatch, selectedChannel }) => {
    useEffect(() => {
        dispatch(fetchVideoPosts(selectedChannel));
    });

    return (
        <div className="container">
            <h1>Hello</h1>
            <ChannelNav channels={['NBA', 'NFL']}/>
            <VideoPostList />
        </div>
    );
}

const mapStateToProps = state => {
    const { selectedChannel, videoPostsByChannel } = state;
    const {
        isFetching,
        lastUpdated,
        items: videoPosts
    } = videoPostsByChannel[selectedChannel] || {
        isFetching: true,
        items: []
    }

    return {
        selectedChannel,
        videoPosts,
        isFetching,
        lastUpdated
    }
}

export default connect(mapStateToProps)(App);