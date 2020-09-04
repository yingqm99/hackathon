
import React from 'react';

import { Input } from 'antd';

class TextBox extends React.Component {

    onChange = (e) => {
        console.log("text changed: ", e);
    }

    render() {
        return (
            <div>
                This is a textbox
                <Input >
                    placeholder="Enter the username"
                </Input>
            </div>
        )
    }
}


export default TextBox;