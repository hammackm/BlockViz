import React, { Component } from 'react';
import axios from "axios";
import { Col, Container, Row } from 'react-bootstrap';
import './style/BlockDetails.scss'

export default class BlockDetails extends Component {
  constructor(props) {
    super(props);
    this.state = {
      block: {height: 0},
    };
  }

  componentDidMount() {
    axios
    .get(`/height/${this.props.match.params.blockHeight}`)
    .then((res) => {this.setState({block: res.data}); console.log(res)})
    .catch((err) => console.log(err));

  }

  render = () => {

    return (
      <main className="container">
        <h2 className="text-black my-4">Block {this.props.match.params.blockHeight}</h2>
        <hr className="headRuler"/>
        <div className="blockdetails">
          <Container>
          <Row>
              <Col><div><b>Hash</b> {this.state.block.hash}</div></Col>
            </Row>
            <hr />
            <Row>
              <Col><b>Difficulty</b> {this.state.block.difficulty}</Col>
              <Col><b>Size</b> {this.state.block.size}</Col>
            </Row>
            <hr />
            <Row>
              <Col><b>Transactions</b> {this.state.block.nTx}</Col>
              <Col><b>Confirmations</b> {this.state.block.confirmations}</Col>
              <Col><b>Nonce</b> {this.state.block.nonce}</Col>
            </Row>
            <hr />
          </Container>
          <h3 className="text-black my-4">Transactions </h3>
          <hr className="bodyRuler"/>
          {this.state.block.tx}

        </div>
      </main>
      );
      };
}