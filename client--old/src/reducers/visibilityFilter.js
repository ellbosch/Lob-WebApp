import { SET_VISIBILITY_FILTER, VisibilityFilters } from '../actions';
const { SELECT_ALL } = VisibilityFilters;

// reducer composition for channel view
function visibilityFilter(state={channel: SELECT_ALL}, action) {
    switch (action.type) {
        case SET_VISIBILITY_FILTER:
            return action;
        default:
            return state;
    }
}

export default visibilityFilter;