import React from 'react';
import { useDispatch } from 'react-redux';
import { NavLink } from 'react-router-dom';
import { selectChannel, fetchVideoPosts } from '../actions';

const ChannelLink = ({ filter, channel, children }) => {
    const dispatch = useDispatch();

    const handleClick = () => {
        dispatch(selectChannel({channel}));
        dispatch(fetchVideoPosts({channel}));
    }

    return (
        <NavLink exact to={filter === 'SELECT_ALL' ? '/' : `/${channel}`}
            onClick={() => handleClick()}>
            {children}
        </NavLink>
    );
}

export default ChannelLink;