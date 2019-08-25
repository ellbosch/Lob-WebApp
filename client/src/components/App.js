import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchVideoPosts } from '../actions';
import ChannelNav from './ChannelNav';
import VideoPostList from './VideoPostList';

const App = () => {
    const dispatch = useDispatch();
    const channel = useSelector(state => state.visibilityFilter.channel);

    // fetches video posts on first load
    useEffect(() => {
        dispatch(fetchVideoPosts(channel));
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