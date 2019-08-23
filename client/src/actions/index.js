import fetch from 'cross-fetch';

// action for visibility filter
export const SET_VISIBILITY_FILTER = 'SET_VISIBILITY_FILTER';

export const VisibilityFilters = {
    SHOW_ALL: 'SELECT_ALL',
    SELECT_CHANNEL: 'SELECT_CHANNEL'
}

export const selectChannel = (channel) => {
    return {
        type: VisibilityFilters.SELECT_CHANNEL,
        channel
    }
}

// action for requesting video posts
export const REQUEST_POSTS = 'REQUEST_POSTS'

const requestPosts = (channel) => {
    return {
        type: REQUEST_POSTS,
        channel
    }
}

// acton for receiving posts
export const RECEIVE_POSTS = 'RECEIVE_POSTS'

const receivePosts = (channel, json) => {
  return {
        type: RECEIVE_POSTS,
        channel,
        posts: json.data,
        receivedAt: Date.now()
  }
}

export function fetchVideoPosts(channel) {
    return function(dispatch) {
        // inform app state that api call is starting
        dispatch(requestPosts(channel));

        return fetch('/video-posts/')
        .then(
            res => res.json(),
            error => console.log('An error occurred.', error)
        )
        .then(result => {
            console.log(result);

            // update app state with results
            dispatch(receivePosts(channel, result))
        })
    }
}
                

// const shouldFetchVideoPosts = (state, channel) => {
//     const posts = state.videoPostsByChannel[channel]
//     if (!posts) {
//         return true
//     }
//     if (posts.isFetching) {
//         return false
//     }
//     return posts.didInvalidate
//     }
// export const fetchVideoPostsIfNeeded = channel => (dispatch, getState) => {
//     if (shouldFetchPosts(getState(), channel)) {
//       return dispatch(fetchPosts(channel))
//     }
//   }