import React from 'react';
import './App.css';

import EmailDate from './components/EmailDate';
import PieChart from './components/PieChart';


class App extends React.Component {
  render() {
    return (
      <div className="App">
        <EmailDate />
        <PieChart />
      </div>
    );
  }
}

export default App;
