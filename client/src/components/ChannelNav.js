import React from 'react';
import ChannelLink from '../containers/ChannelLink';
import { VisibilityFilters } from '../actions';

const ChannelNav = (channels) => (
    <ul className="nav flex-column">
        <li className="nav-item">
            <ChannelLink channel={VisibilityFilters.SHOW_ALL}>All</ChannelLink>
        </li>
        <li className="nav-item">
            <ChannelLink channel="nba">NBA</ChannelLink>
        </li>
        <li className="nav-item">
            <ChannelLink channel="nfl">NFL</ChannelLink>
        </li>
    </ul>
);

export default ChannelNav;
