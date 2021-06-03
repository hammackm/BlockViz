import React, { Component } from 'react';
import {OverlayTrigger}  from 'react-bootstrap';
import { InfoCircle } from 'react-bootstrap-icons';
import { HeaderPopover} from './index'
import './style/Overlay.scss';

export default class BlockHeightOverlay extends Component {

  render = () => {

    return (
        <OverlayTrigger trigger="hover" placement="right" overlay={<HeaderPopover {...this.props}/>}>
            <InfoCircle />
        </OverlayTrigger>
        );
    };
}