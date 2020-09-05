
import React, {Component} from 'react';
// import * as d3 from "d3";
import { PieChart } from 'react-chartkick';
import 'chart.js';

class pieChart extends Component {
    
    constructor(props) {
        super(props);
        this.state = { data: {}};
    }
    // this.state = { data: {} };
              
    
    componentDidMount(){

        fetch('/email', { credentials: 'same-origin' })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
            var count = 0;
            var dict = {};

            for (var key in data){
                if (!(key in dict) && isNaN(key) && key){
                    dict[key]['tone_name'] = 1;
                }
                else if (key in dict){
                    dict[key]['tone_name'] = dict[key]['tone_name'] + 1;
                }
                count = count + 1;
                if (count === 30) {
                    break;
                }
            }
            
            // data: {tone_name: count, ...}
            
          this.setState({
            data: dict,
          });
        })
        .catch((error) => console.log(error));
    }

    render(){
        const { data } = this.state;
        var emotion = [];
        for (var key in data){
            var tempList = [];
            tempList.push(key);
            tempList.push(data[key]);
            emotion.push(tempList);
        }

        return (
            <div className="piechart">
                 <PieChart data={emotion}/>
            </div>
        );
    }
}
export default pieChart;
