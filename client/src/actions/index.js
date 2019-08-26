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

const receivePosts = (channel, json) => {
  return {
        type: RECEIVE_POSTS,
        channel,
        items: json.results,
        receivedAt: Date.now()
    }
}

// fetches videos given a specified channel and page
export function fetchVideoPosts(channel, page=0) {
    return function(dispatch) {
        // inform app state that api call is starting
        dispatch(requestPosts(channel));

        const apiPath = (channel !== '') ? '/api/v1/posts?channel=' + channel + '&page=' + page : 'api/v1/posts';

        return fetch(apiPath)
            .then(
                res => res.json(),
                error => console.log('An error occurred.', error)
            )
            .then(result => {
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