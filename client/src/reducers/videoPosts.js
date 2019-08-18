import { TOGGLE_CHANNEL } from './actions';

// reducer composition for channels
function channel(state=null, action) {
    switch (action.type) {
        case TOGGLE_CHANNEL:
            return action.channel;
        default:
            return state;
    }
}

export default channel;