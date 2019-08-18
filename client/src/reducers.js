import { combineReducers } from 'redux';
import { TOGGLE_CHANNEL, SET_VISIBILITY_FILTER, VisibilityFilters } from './actions';
const { SHOW_ALL } = VisibilityFilters;

// reducer composition for filter view
function visibilityFilter(state=SHOW_ALL, action) {
    switch (action.type) {
        case SET_VISIBILITY_FILTER:
            return action.filter;
        default:
            return state;
    }
}

// reducer composition for channels
function channel(state=null, action) {
    switch (action.type) {
        case TOGGLE_CHANNEL:
            return action.channel;
        default:
            return state;
    }
}

// main app reducer
const app = combineReducers({
    visibilityFilter,
    channel
});

export default app;