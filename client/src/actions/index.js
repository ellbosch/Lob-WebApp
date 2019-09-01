import fetch from 'cross-fetch';

// action for visibility filter
export const SET_VISIBILITY_FILTER = 'SET_VISIBILITY_FILTER';

export const VisibilityFilters = {
    SELECT_ALL: 'SELECT_ALL',
    SELECT_CHANNEL: 'SELECT_CHANNEL'
}

export const selectAllChannels = () => {
    return {
        type: SET_VISIBILITY_FILTER,
        filter: VisibilityFilters.SELECT_ALL,
        channel: ''
    }
}

export const selectChannel = (channel) => {
    return {
        type: SET_VISIBILITY_FILTER,
        filter: VisibilityFilters.SELECT_CHANNEL,
        channel
    }
}

// clear posts (when we select a new channel)
export const CLEAR_POSTS = 'CLEAR_POSTS';

export const clearPosts = () => {
    return {
        type: CLEAR_POSTS
    }
}

// action for requesting video posts
export const REQUEST_POSTS = 'REQUEST_POSTS';

const requestPosts = (channel) => {
    return {
        type: REQUEST_POSTS,
        channel
    }
}

// action for receiving posts
export const RECEIVE_POSTS = 'RECEIVE_POSTS';

const receivePosts = (channel, items) => {
  return {
        type: RECEIVE_POSTS,
        channel,
        items,
        receivedAt: Date.now()
    }
}

// fetches videos given a specified channel and page
export function fetchVideoPosts(channel) {
    return function(dispatch, getState) {
        // inform app state that api call is starting
        dispatch(requestPosts(channel));

        // get page for pagination
        const page = getState().videoPostsByChannel.page;

        const apiPath = (channel !== '') ? '/api/v1/posts?channel=' + channel + '&page=' + page : 'api/v1/posts';

        return fetch(apiPath)
            .then(
                res => res.json(),
                res => res,
                error => console.log('An error occurred.', error)
            )
            .then(json => {
                const currentItems = getState().videoPostsByChannel.items;

                // append new results to current state of videos
                const items = [...currentItems, ...json.results]
                // update app state with results
                dispatch(receivePosts(channel, items))
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