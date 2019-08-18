import React, { useEffect, useState } from 'react';

function App() {
    const [videoPosts, setVideoPosts] = useState([]);

    useEffect(() => {
        fetch('/video-posts/')
            .then(res => res.json())
            .then(
                (result) => {
                    console.log(result);
                }
            )
    });
    return (
        <div>
        </div>
    );
}

export default App;
