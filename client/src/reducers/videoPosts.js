import { REQUEST_POSTS, RECEIVE_POSTS } from '../actions';

// reducer composition for channels
function videoPosts(
    state={
        isFetching: false,
        items: []
    }, action) {

    switch (action.type) {
        case REQUEST_POSTS:
            return Object.assign({}, state, {
                isFetching: true
            });
        case RECEIVE_POSTS:
            return Object.assign({}, state, {
                isFetching: false,
                items: action.posts,
                lastUpdate: action.received_at
            });
        default:
            return state;
    }
}

function videoPostsByChannel(state={}, action) {
    switch (action.type) {
        case RECEIVE_POSTS:
        case REQUEST_POSTS:
            return Object.assign({}, state, {
                [action.channel]: videoPosts(state[action.channel], action)
            });
        default:
            return state;
    }
}

export default videoPostsByChannel;