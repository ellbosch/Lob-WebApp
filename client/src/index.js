import React from 'react';
import ReactDOM from 'react-dom';
import thunkMiddleware from 'redux-thunk';
import { createLogger } from 'redux-logger';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { createStore, applyMiddleware } from 'redux';
import { Provider } from 'react-redux';
// import { selectChannel, fetchVideoPosts } from './actions';
import rootReducer from './reducers';
import App from './containers/App';
import * as serviceWorker from './serviceWorker';

// CSS
import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

// JS
import 'jquery';
import 'bootstrap/dist/js/bootstrap.js';

const loggerMiddleware = createLogger();

const store = createStore(
    rootReducer,
    applyMiddleware(
        thunkMiddleware,
        loggerMiddleware
    )
);

// store.dispatch(selectChannel('nba'));
// store.dispatch(fetchVideoPosts('nba')).then(() => console.log(store.getState()));

ReactDOM.render(
    <Provider store={store}>
        <Router>
            <Route path="/" component={App} />
        </Router>
    </Provider>,
    document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
