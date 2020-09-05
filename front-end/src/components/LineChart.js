
import React, {Component} from 'react';
// import * as d3 from "d3";
import { LineChart } from 'react-chartkick';
import 'chart.js';

class lineChart extends Component {
    
    constructor(props) {
        super(props);
        this.state = { data: {} };
    }
    // this.state = { data: {} };
              
    
    componentDidMount(){
        //fetch url 
        fetch('/email', { credentials: 'same-origin' })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
            var count = 0;
            var dict = {};
            
            // for (var key, value in data){
            for (var key in data){
                // dict[key] = value['count'];
                dict[key] = data[key]['count'];
                count = count + 1;
                if (count === 30) {
                    break;
                }
            }
          this.setState({
            data: dict,
          });
        })
        .catch((error) => console.log(error));
    }

    render(){
        const { data } = this.state;

        return (
            <div className="linechart">
                 <LineChart data={data}/>
            </div>
        );
    }
}
export default lineChart;
