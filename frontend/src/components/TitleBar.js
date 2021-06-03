import React, { Component } from 'react';
import { Navbar, Nav} from 'react-bootstrap';


export default class TitleBar extends Component {
    render = () => {
    
        return (
          <Navbar bg="dark" variant="dark" sticky="top">
            <Navbar.Brand href="/">BlockViz</Navbar.Brand>
            <Nav className="mr-auto">
              <Nav.Link href="/">Most Recent</Nav.Link>
              <Nav.Link href="/livechain"><b>LiveChain</b></Nav.Link>
              <Nav.Link href="/analytics">Analytics</Nav.Link>
              <Nav.Link href="/about">About</Nav.Link>
            </Nav>
          </Navbar>
        );
      };
}