// // action types
// export const SET_VISIBILITY_FILTER = 'SET_VISIBILITY_FILTER';

// // other constants
// export const VisibilityFilters = {
//     SHOW_ALL: 'SHOW_ALL',
//     SHOW_NBA: 'nba',
//     SHOW_NFL: 'nfl'
// }


// action for selecting channel
export const SELECT_CHANNEL = 'SELECT_CHANNEL';

export const selectChannel = (channel) => {
    return {
        type: SELECT_CHANNEL,
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
    posts: json.data.children.map(child => child.data),
    receivedAt: Date.now()
  }
}