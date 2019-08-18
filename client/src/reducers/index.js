import { combineReducers } from 'redux';
// import videoPosts from './videoPosts';
import visibilityFilter from './visibilityFilter.js';

// main app reducer
export default combineReducers({
    visibilityFilter,
    videoPosts: []
});