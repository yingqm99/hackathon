
import React from 'react';
//import { Input } from 'antd';
import { LineChart, Timeline, ColumnChart, AreaChart } from 'react-chartkick';
import 'chart.js';
import EmailDate from './EmailDate';
import PieChart from './PieChart';
import PersonalRelation from './PersonalRelation';
import {InputGroup, FormControl, Badge} from 'react-bootstrap'

class TextBox extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            // user input
            userInput: '',
            // graph
            dates: [],
            scores: [],
            tones: []
        }
    }

    onChange = (e) => {
        console.log(e.target.value);
    } 

    submitText = () => {
        // console.log("submit to server!");

        // json response format
        // {
        //     "data": [
        //       {
        //         "date": "Fri, 04 Sep 2020 21:01:23 +0000 (UTC)", 
        //         "emailid": "1745aec9cc4564f4", 
        //         "score": 0.686032, 
        //         "tone": "Confident"
        //       }
        //       ...
        // }
        fetch('/email')
            .then((res) => res.json()
            .then((data) => {
                const emails = data.data;
                emails.forEach((email, index) => {
                    const { date, score, tone } = email
                    // console.log(`${date}:${score}:${typeof(tone)}`);
                    this.setState((prevState) => ({
                        dates: [...prevState.dates, date],
                        scores: [...prevState.scores, parseFloat(score)],
                        tones: [...prevState.tones, tone]
                    }));
                })
            })
        )

    }

    render() {
        const { dates, scores, tones } = this.state;

        const lineChartData = dates.map((date, index) => {
            // console.log(date, index);
            return ([date, scores[index]]);
        });


        // console.log(lineChartData)

        return (
            <div>
                
                <div>
                  <h1>
                    Example heading
                    <Badge variant="secondary">New</Badge>
                  </h1>
                  
                  
                  <InputGroup size="lg" className="mb-3">
                    <InputGroup.Prepend>
                      <InputGroup.Text id="basic-addon1">@</InputGroup.Text>
                    </InputGroup.Prepend>
                    <FormControl
                      placeholder="Enter your email to analyze: "
                      aria-label="text"
                      aria-describedby="basic-addon1"
                    />
                  </InputGroup>

            

                  
                </div>
                
                <p>Press enter to submit</p>
                
                <LineChart data={lineChartData} />
                
                <EmailDate />
                
                <PieChart />

                <PersonalRelation />
            </div>
        )
    }
}


export default TextBox;
