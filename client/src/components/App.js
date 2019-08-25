import React, { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { selectAllChannels, fetchVideoPosts } from '../actions';
import ChannelNav from './ChannelNav';
import VideoPostList from './VideoPostList';

const App = () => {
    const dispatch = useDispatch();

    // fetches trending video posts on first load
    useEffect(() => {
        dispatch(selectAllChannels());
        dispatch(fetchVideoPosts(''));
    }, []);

    return (
        <div className="container">
            <h1>Hello</h1>
            <ChannelNav channels={['NBA', 'NFL']} />
            <VideoPostList />
        </div>
    );
}

export default App;