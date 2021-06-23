import React, { Component } from 'react';
import axios from "axios";
import { Col, Container, Row, Card } from 'react-bootstrap';
//import './style/TransactionDetails.scss'

export default class WalletDetails extends Component {
  constructor(props) {
    super(props);
    this.state = {
      wallet: {},
    };
  }

  componentDidMount() {

  }

  render = () => {

    return (
      <main className="container">
        <h2 className="text-black my-4">Wallet: {this.props.match.params.address}</h2>
        <div className="blockdetails">
        </div>
      </main>
      );
      };
}