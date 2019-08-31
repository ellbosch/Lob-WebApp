import React from 'react';
import { NavLink } from 'react-router-dom';

const ChannelLink = ({ filter, channel, handleClick, children }) => {
    return (
        <NavLink exact to={filter === 'SELECT_ALL' ? '/' : `/${channel}`}
            onClick={() => handleClick(channel)}>
            {children}
        </NavLink>
    );
}

export default ChannelLink;