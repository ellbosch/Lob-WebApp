import React from 'react';
import ChannelLink from '../containers/ChannelLink';
import { VisibilityFilters } from '../actions';

const ChannelNav = ({channels}) => (
    <ul className="nav flex-column">
        <li className="nav-item">
            <ChannelLink filter={VisibilityFilters.SELECT_ALL} key="SELECT_ALL">All</ChannelLink>
        </li>
        {channels.map(channel =>
            <li className="nav-item">
                <ChannelLink filter={VisibilityFilters.SELECT_CHANNEL} key={channel} channel={channel}>{channel}</ChannelLink>
            </li>)
        }
    </ul>
);

export default ChannelNav;
