import React from 'react';
import './App.css';

import EmailDate from './components/EmailDate';
import TextBox from './components/TextBox';

class App extends React.Component {
  render() {
    return (
      <div className="App">
        <EmailDate />
        
      </div>
    );
  }
}

export default App;
