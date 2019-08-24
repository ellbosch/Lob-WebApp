import { combineReducers } from 'redux';
import videoPosts from './videoPosts';
import visibilityFilter from './visibilityFilter.js';

// main app reducer
const rootReducer = combineReducers({
    visibilityFilter,
    videoPosts
});

export default rootReducer;