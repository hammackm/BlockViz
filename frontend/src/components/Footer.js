import React, { Component } from 'react';
import { Navbar, Nav} from 'react-bootstrap';
import './style/Footer.scss'; //style can be used as className="bvFooter" or bsPrefix="bvFooter" ||| className kept some bs styling while bsPrefix did not


export default class Footer extends Component {
    render = () => {
    
        return (
            <Navbar className="bvFooter" style={{backgroundColor: '#198652'}} variant="dark" sticky="bottom">
                <Nav className="me-auto">
                    <Nav.Link href="/">BlockViz</Nav.Link>
                </Nav>
                <Navbar.Collapse className="justify-content-end">
                    <Navbar.Text>
                        Pre-Alpha 0.0.1
                    </Navbar.Text>
                </Navbar.Collapse>
          </Navbar>
        );
      };
}