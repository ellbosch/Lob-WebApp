import React, { useEffect } from 'react';

function App() {

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
            <h1>Hello</h1>
        </div>
    );
}

export default App;
