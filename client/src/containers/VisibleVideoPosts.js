import { connect } from react-redux;
import VideoPostList from '../components/VideoPostList';
import { VisibilityFilters } from '../actions';

const getVisibleVideoPosts = (videoPosts, filter) => {
    switch (filter) {
        case VisibilityFilters.SHOW_ALL:
            return videoPosts
        default:
            throw new Error('Unknown filter: ' + filter)
    }
}

const mapStateToProps = state => ({
    videoPosts: getVisibleVideoPosts(state.videoPosts, state.visibilityFilter)
});

export default connect(mapStateToProps)(VideoPostList);