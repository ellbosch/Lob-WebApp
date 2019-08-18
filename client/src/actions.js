// action types
export const TOGGLE_CHANNEL = 'TOGGLE_CHANNEL'
export const SET_VISIBILITY_FILTER = 'SET_VISIBILITY_FILTER'

// other constants
export const VisibilityFilters = {
    SHOW_ALL: 'SHOW_ALL',
    SHOW_ONE: 'SHOW_ONE'
}

// action creators
export function changeSport(sport) {
    return { type: CHANGE_SPORT, sport }
}