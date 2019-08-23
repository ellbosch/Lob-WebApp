import { SET_VISIBILITY_FILTER, VisibilityFilters } from '../actions';
const { SELECT_ALL } = VisibilityFilters;

// reducer composition for filter view
function visibilityFilter(state=SELECT_ALL, action) {
    switch (action.type) {
        case SET_VISIBILITY_FILTER:
            return action.filter;
        default:
            return state;
    }
}

export default visibilityFilter;