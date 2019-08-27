import React from 'react';
import { useDispatch } from 'react-redux';
import ChannelLink from '../containers/ChannelLink';
import { VisibilityFilters, clearPosts, selectChannel, selectAllChannels, fetchVideoPosts } from '../actions';

const ChannelNav = ({channels}) => {
    const dispatch = useDispatch();

    const handleClickForAll = () => {
        dispatch(clearPosts());
        dispatch(selectAllChannels());
        dispatch(fetchVideoPosts(''));
    }

    const handleClickForChannel = (channel) => {
        dispatch(clearPosts());
        dispatch(selectChannel(channel));
        dispatch(fetchVideoPosts(channel));
    }

    return (
        <ul className="nav flex-column">
            <li className="nav-item" key="SELECT_ALL">
                <ChannelLink filter={VisibilityFilters.SELECT_ALL} channel='' handleClick={handleClickForAll}>All</ChannelLink>
            </li>
            {channels.map(channel =>
                <li className="nav-item" key={channel}>
                    <ChannelLink filter={VisibilityFilters.SELECT_CHANNEL} channel={channel} handleClick={handleClickForChannel}>{channel}</ChannelLink>
                </li>)
            }
        </ul>
    )
}

export default ChannelNav;
