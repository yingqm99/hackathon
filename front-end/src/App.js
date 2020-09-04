import React from 'react';
import './App.css';

import TextBox from './components/TextBox';


class App extends React.Component {
  render() {
    return (
      <div className="App">
        <TextBox />
      </div>
    );
  }
}

export default App;
