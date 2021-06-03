import React, { Component } from 'react';
import {OverlayTrigger, Popover}  from 'react-bootstrap';
import { InfoCircle } from 'react-bootstrap-icons';
import { HeaderPopover} from './index'
import './style/Overlay.scss';

export default class HeaderOverlay extends Component {
    constructor(props) {
        super(props);
      }

  render = () => {

    return (
        <OverlayTrigger trigger="hover" placement="right" overlay={<HeaderPopover {...this.props}/>}>
            <InfoCircle />
        </OverlayTrigger>
        );
    };
}