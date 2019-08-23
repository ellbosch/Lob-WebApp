import { combineReducers } from 'redux';
import videoPosts from './videoPosts';
// import selectChannel from './selectChannel';
import visibilityFilter from './visibilityFilter.js';

// main app reducer
export default combineReducers({
    videoPosts,
    visibilityFilter
});