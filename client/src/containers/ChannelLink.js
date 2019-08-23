import React from 'react';
import { connect } from 'react-redux';
import { NavLink } from 'react-router-dom';
import { setVisibilityFilter } from '../actions';

const ChannelLink = ({ channel, children }) => (
    <NavLink exact to={channel === 'SELECT_ALL' ? '/' : `/${channel}`}>
        {children}
    </NavLink>
);

export default ChannelLink;