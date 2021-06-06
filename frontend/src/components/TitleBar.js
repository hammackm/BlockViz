import React, { Component } from 'react';
import { Navbar, Nav} from 'react-bootstrap';
import axios from "axios";


export default class TitleBar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      vtcPriceInUsd: 0.00
    };
  }

  componentDidMount() {
    //axios
    //.get('https://api.coinbase.com/v2/prices/BTC-USD/spot')
    //.then((res) => this.setState({vtcPriceInUsd: res.data.data.amount}))
    //.catch((err) => console.log(err));
  }

    render = () => {
    
        return (
          <Navbar style={{backgroundColor: '#198652'}} variant="dark" sticky="top">
            <Navbar.Brand href="/">BlockViz</Navbar.Brand>
            <Nav className="mr-auto">
              <Nav.Link href="/">Blocks</Nav.Link>
              <Nav.Link href="/transactions">Transactions</Nav.Link>
              <Nav.Link href="/analytics">Analytics</Nav.Link>
              <Nav.Link href="/about">About</Nav.Link>
            </Nav>
            <Navbar.Collapse className="justify-content-end">
              <Navbar.Text>
                1 BTC (shitty exchanges not having vtc api) = ${this.state.vtcPriceInUsd}
              </Navbar.Text>
            </Navbar.Collapse>
          </Navbar>
        );
      };
}