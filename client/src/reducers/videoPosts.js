import { SELECT_CHANNEL, REQUEST_POSTS, RECEIVE_POSTS } from './actions';

// reducer composition for channels
function videoPosts(
    state={
        isFetching: false,
        items: []
    }, action) {

    switch (action.type) {
        // case SELECT_CHANNEL:
        //     return Object.assign({}, state, {
        //         isFetching: true
        //     });
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

export default videoPosts;