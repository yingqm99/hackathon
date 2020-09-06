
import React, {Component} from 'react';
// import * as d3 from "d3";
import { ColumnChart } from 'react-chartkick';
import 'chart.js';
import { Container, Row, Col } from 'react-bootstrap';


class PersonalRelation extends Component {
    
    constructor(props) {
        super(props);
        this.state = { data: [], data_like_most: [], };
    }
    // this.state = { data: {} };
              
    
    componentDidMount(){
        
        fetch('/personal_relations', { credentials: 'same-origin' })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            var count = 0;
            var dict = [];
            var dict_most_like = [];
            console.log(data.data);
            var temp = [];
            temp = data.data;
            temp.sort(function(a,b){return a['score']-b['score']});
            //var most_like = data.data;
            //most_like.sort(function(a,b){return b['score']-a['score']});
            var i;
            for (i = 0; i < temp.length; ++i){
                var tempList = [];
                console.log(temp[i]);
                tempList.push(temp[i]['person_name']);
                tempList.push(temp[i]['score']);
                dict.push(tempList);
                tempList = [];
                console.log(temp[temp.length-i]);
                tempList.push(temp[temp.length-i-1]['person_name']);
                tempList.push(temp[temp.length-i-1]['score']);
                dict_most_like.push(tempList);
                if (i===10) {break;}
            }
            
            
            // store in localStorage
            localStorage.setItem('PersonalRelationData', dict);

            this.setState({
            data: dict,
            data_like_most: dict_most_like,
            });
        })
        .catch((error) => console.log(error));
    
    }

    render(){
        const { data } = this.state;
        const { data_like_most } = this.state;
        return (
            <div className="histogram">

                <Container>
                    <Row>
                        <Col>
                         <h3>Top 10 Favoriate People</h3>
                         <ColumnChart data={data_like_most}/>
                        </Col>
                        <Col>
                         <h3>Least 10 Favoriate People</h3>
                         
                         <ColumnChart data={data}/>
                        </Col>
                    </Row>
                </Container>
                
            </div>
        );
    }
}
export default PersonalRelation;
