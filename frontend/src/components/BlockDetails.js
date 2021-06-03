import React, { Component } from 'react';

export default class BlockDetails extends Component {

  render = () => {

    return (
        <div className="block details">
          <div class="container">
            <h1 class="font-weight-light">About</h1>
            <p>
                Lorem Ipsum is simply dummy text of the printing and typesetting
                industry. Lorem Ipsum has been the industry's standard dummy text
                ever since the 1500s, when an unknown printer took a galley of
                type and scrambled it to make a type specimen book.
            </p>
            <p>Block: {this.props.block.height}</p>
          </div>
        </div>
      );
      };
}