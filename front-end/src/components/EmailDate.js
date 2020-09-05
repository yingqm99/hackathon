
import React, {Component} from 'react';
// import * as d3 from "d3";
import { LineChart } from 'react-chartkick';
import 'chart.js';
import ListItems from './ListItems';
import PieChart from './PieChart';
// import PersonalRelation from './PersonalRelation';

import '../styles/EmailDate.css';
import PersonalRelation from './PersonalRelation';
import Change from './Change';
import { obj } from 'pumpify';

class EmailDate extends Component {
    
    constructor(props) {
        super(props);
        this.state = { 
            data: {} ,
            emails: []
        };
    }
    // this.state = { data: {} };

    componentDidMount(){
        // get from localStorage
        if (Object.keys(this.state.data).length != 0 && this.state.data.constructor === Object) {
            this.setState({
                data: localStorage.getItem('EmailDateData')
            });
            console.log("email cache: ", this.state.data);
        } else {
            //fetch url 
            fetch('/email', { credentials: 'same-origin' })
            .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
            })
            .then((data) => {
                console.log("/email data", data.data);

                var count = 0;
                var dict = {};
                
                var i;
                for (i = 0; i < data.data.length; ++i){
                    console.log(data.data[i]);
                    if(!(data.data[i]['date'] in dict)){
                        dict[data.data[i]['date']] = 1;
                        count = count + 1;
                    }
                    else{
                        dict[data.data[i]['date']] = dict[data.data[i]['date']] + 1;
                    }
                    if (count === 30){
                        break;
                    }
                }

                console.log("/email dict", dict);
                
            // store in localStorage
            localStorage.setItem('EmailDateData', dict);

            this.setState({
                data: dict,
                emails: data.data
            });
            })
            .catch((error) => console.log(error));
        }
    }

    render(){
        const { data, emails } = this.state;

        return (
            <div className="emaildate">
                <div className="listitems">
                    <ListItems emails={emails} />
                </div>
                <div className="content">
                    <div className="linecharts">
                        <PieChart />
                        <br />
                        <br />
                        <LineChart data={data} height={450} width={900}/>
                        <br />
                        <br />
                        <Change />
                    </div>
                    {/* <div className="piecharts">
                         <PieChart />
                    </div> */}
                </div>

                {/* <div>
                    <PersonalRelation
                </div> */}
                
            </div>
        );
    }
}
export default EmailDate;
