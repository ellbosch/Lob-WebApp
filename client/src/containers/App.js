import React from 'react';
import ChannelNav from '../components/ChannelNav';
import VideoPostList from '../components/VideoPostList';

const App = () => {
    // useEffect(() => {
    //     dispatch(fetchVideoPosts(selectedChannel));
    // });



    return (
        <div className="container">
            <h1>Hello</h1>
            <ChannelNav channels={['NBA', 'NFL']} />
            <VideoPostList />
        </div>
    );
}

export default App;