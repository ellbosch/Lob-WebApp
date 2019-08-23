import { SELECT_CHANNEL } from '../actions';

function selectChannel(state='', action) {
    switch (action.type) {
        case SELECT_CHANNEL:
            return action.channel;
        default:
            return state;
    }
}

export default selectChannel;