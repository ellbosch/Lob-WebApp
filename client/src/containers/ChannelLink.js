import React from 'react';
import { useDispatch } from 'react-redux';
import { NavLink } from 'react-router-dom';
import { selectChannel } from '../actions';

const ChannelLink = ({ filter, channel, children }) => {
    const dispatch = useDispatch();

    return (
        <NavLink exact to={filter === 'SELECT_ALL' ? '/' : `/${channel}`}
            onClick={() => dispatch(selectChannel({channel}))}>
            {children}
        </NavLink>
    );
}

export default ChannelLink;