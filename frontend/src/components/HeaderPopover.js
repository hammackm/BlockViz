import React, { Component } from 'react';
import {Popover}  from 'react-bootstrap';

export default class headerPopover extends Component {

  render = () => {

    return (
        <Popover id="popover-basic">
            <Popover.Title as="h3">Placeholder text</Popover.Title>
            <Popover.Content>
                And here's some <strong>amazing</strong> content. It's very engaging.
                right?
            </Popover.Content>
        </Popover>
        );
    };
}