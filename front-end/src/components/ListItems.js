import React from 'react';
import App from '../App';
import '../styles/EmailDate.css';
import { Tooltip } from 'antd';

// props: date, text, tone
class Item extends React.Component {
    render() {
        const { date, text, tone } = this.props;
        return(
            <div className="item">
               <p>Date: <strong>{date}</strong> Tone: <strong>{tone}</strong></p>
               <p>Text: {text}</p>
            </div>
        )
    }
}

// props: emails
class ListItems extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {

        const items = this.props.emails.map((email, index) => {
            const {date, text, tone} = email;
            return(
                <Item key={index} date={date} text={text} tone={tone} />
            );
        })

        console.log("items: ", items);

        return (
            <div>{items}</div>
        )
    }
}

export default ListItems;