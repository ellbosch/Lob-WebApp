import React from 'react';
import { NavLink } from 'react-router-dom';

type ClickCallback = (channel?: string) => any;

interface ChannelLinkProps {
    filter: string,
    channel?: string,
    handleClick: ClickCallback,
    children: string
}

const ChannelLink = ({filter, channel, handleClick, children}: ChannelLinkProps) => {
    return (
        <NavLink exact to={filter === 'SELECT_ALL' ? '/' : `/${channel}`}
            onClick={() => handleClick(channel)}>
            {children}
        </NavLink>
    );
}

export default ChannelLink;