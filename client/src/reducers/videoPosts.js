import { REQUEST_POSTS, RECEIVE_POSTS, CLEAR_POSTS } from '../actions';

// reducer composition for channels
function videoPosts(
    state={
        isFetching: false,
        items: [],
        page: 0
    }, action) {

    switch (action.type) {
        case CLEAR_POSTS:
            return Object.assign({}, state, {
                items: [],
                page: 0
            });
        case REQUEST_POSTS:
            return Object.assign({}, state, {
                isFetching: true
            });
        case RECEIVE_POSTS:
            return Object.assign({}, state, {
                isFetching: false,
                items: action.items,
                page: state.page + 1,
                lastUpdate: action.received_at
            });
        default:
            return state;
    }
}

function videoPostsByChannel(state={ items: [] }, action) {
    switch (action.type) {
        case CLEAR_POSTS:
        case RECEIVE_POSTS:
        case REQUEST_POSTS:
            return videoPosts(state, action);
        default:
            return state;
    }
}

export default videoPostsByChannel;