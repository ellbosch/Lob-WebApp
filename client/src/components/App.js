import React from 'react';
// import { useDispatch, useSelector } from 'react-redux';
import ChannelNav from './ChannelNav';
import VideoPostList from './VideoPostList';

function App() {
    // const dispatch = useDispatch();
    // const videoPosts = useSelector(videoPosts => state.videoPosts);

    // useEffect(() => {
    //     fetch('/video-posts/')
    //         .then(res => res.json())
    //         .then(
    //             (result) => {
    //                 console.log(result);
    //             }
    //         )
    // });
    return (
        <div className="container">
            <h1>Hello</h1>
            <ChannelNav />
            <VideoPostList />
        </div>
    );
}

export default App;
