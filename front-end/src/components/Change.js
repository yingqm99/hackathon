
import React, {Component} from 'react';
// import * as d3 from "d3";
import { BarChart } from 'react-chartkick';
import 'chart.js';

class Change extends Component {
    
    constructor(props) {
        super(props);
        this.state = { data: [] };
    }
    // this.state = { data: {} };
              
    
    componentDidMount(){
        // get from localStorage
        if (Object.keys(localStorage.getItem('ChangeEmotionDat')).length !== 0) {
            this.setState({
                data: localStorage.getItem('ChangeEmotionDat')
            });
        } else {
            // fetch url
            fetch('/change_of_emotions', { credentials: 'same-origin' })
            .then((response) => {
              if (!response.ok) throw Error(response.statusText);
              return response.json();
            })
            .then((data) => {
                console.log(data.data);
                var list = data.data;
                var dict = [];
                var i;
                for (i = 0; i < list.length; ++i){
                    var temp_list = [];
                    temp_list.push(list[i]['tone_name']);
                    temp_list.push(list[i]['change']);
                    dict.push(temp_list);
                }
                console.log(dict);
    
              // store in localStorage
              localStorage.setItem('ChangeEmotionData', dict);
    
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
            <div className="histogram">
                 <BarChart data={data}/>
            </div>
        );
    }
}
export default Change;
