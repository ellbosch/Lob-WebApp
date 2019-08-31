import { combineReducers } from 'redux';
import videoPostsByChannel from './videoPosts';
import visibilityFilter from './visibilityFilter.js';

// main app reducer
const rootReducer = combineReducers({
    visibilityFilter,
    videoPostsByChannel
});

export default rootReducer;