import React, { Component } from 'react';
import {Table, Button} from 'react-bootstrap';

export default class About extends Component {

  render = () => {

    return (
        <div className="about">
          <div class="container">
            <h1 class="font-weight-light">About</h1>
            <p>
                Lorem Ipsum is simply dummy text of the printing and typesetting
                industry. Lorem Ipsum has been the industry's standard dummy text
                ever since the 1500s, when an unknown printer took a galley of
                type and scrambled it to make a type specimen book.
            </p>
          </div>
        </div>
      );
      };
}