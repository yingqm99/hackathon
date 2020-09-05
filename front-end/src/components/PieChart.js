
import React, {Component} from 'react';
// import * as d3 from "d3";
import { PieChart } from 'react-chartkick';
import 'chart.js';


class pieChart extends Component {
    
    constructor(props) {
        super(props);
        this.state = { data: [] };
    }
    // this.state = { data: {} };
              
    
    componentDidMount(){
        
        if (Object.keys(this.state.data).length == 0 && this.state.data.constructor === Object) {
            this.setState({
                data: localStorage.getItem('pieChartData')
            });
        } else {
            // fetch url
            fetch('/recent_emotions', { credentials: 'same-origin' })
            .then((response) => {
              if (!response.ok) throw Error(response.statusText);
              return response.json();
            })
            .then((data) => {
                var count = 0;
                var dict = [];
                // console.log(data.data);
                
                var i;
                for (i = 0; i < data.data.length; ++i){
                    var tempList = [];
                    // console.log(data.data[i]);
                    tempList.push(data.data[i]['tone_name']);
                    tempList.push(data.data[i]['count']);
                    dict.push(tempList);
                }
    
              // store in localStorage
              localStorage.setItem('pieChartData', dict)
              
              this.setState({
                data: dict,
              });
            })
            .catch((error) => console.log(error));

        }
    }

    render(){
        const { data } = this.state;

        return (
            <div className="piechart">
                 <PieChart data={data}/>
            </div>
        );
    }
}
export default pieChart;
