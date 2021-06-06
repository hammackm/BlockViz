import React, { Component } from 'react';
import axios from "axios";
import { Col, Container, Row, Spinner, Alert } from 'react-bootstrap';
import {Transaction} from './index'
import './style/BlockDetails.scss'

export default class BlockDetails extends Component {
  constructor(props) {
    super(props);
    this.state = {
      block: {height: 0},
      transactions: [],
      transactionsLoading: true,
    };
  }

  componentDidMount() {
    axios
    .get(`/height/${this.props.match.params.blockHeight}`)
    .then((res) => this.setState({block: res.data}))
    .catch((err) => console.log(err));

    axios
    .get(`/transactions/${this.props.match.params.blockHeight}`)
    .then((res) => this.setState({
      transactions: res.data,
      transactionsLoading: false
    }))
    .catch((err) => console.log(err));

  }

  render = () => {

    return (
      <main className="container">
        <h2 className="text-black my-4">Block: {this.props.match.params.blockHeight}</h2>
        <div className="blockdetails">
          <Container>
            <Row>
              <Col><div><p className="alignLeft">Hash</p> <p className="alignRight">{this.state.block.hash}</p></div><hr className="columnRuler"/></Col>
            </Row>
            <Row>
              <Col><div><p className="alignLeft">Previous Block Hash</p> <p className="alignRight">{this.state.block.previousblockhash}</p></div><hr className="columnRuler"/></Col>
            </Row>
            <Row>
              <Col><div><p className="alignLeft">Next Block Hash</p> <p className="alignRight">{this.state.block.nextblockhash}</p></div><hr className="columnRuler"/></Col>
            </Row>
            <Row>
              <Col><div><p className="alignLeft">Merkle Root</p> <p className="alignRight">{this.state.block.merkleroot}</p></div><hr className="columnRuler"/></Col>
            </Row>
            <hr className="bodyRuler"/>
            <Row>
              <Col><p className="alignLeft">Difficulty</p> <p className="alignRight">{this.state.block.difficulty}</p><hr className="columnRuler"/></Col>
              <Col><p className="alignLeft">Version</p> <p className="alignRight">{this.state.block.version}</p><hr className="columnRuler"/></Col>
            </Row>
            <Row>
              <Col><p className="alignLeft">Timestamp</p> <p className="alignRight">{this.state.block.time}</p><hr className="columnRuler"/></Col>
              <Col><p className="alignLeft">Median Time</p> <p className="alignRight">{this.state.block.mediantime}</p><hr className="columnRuler"/></Col>
            </Row>
            <hr className="bodyRuler"/>
            <Row>
              <Col><p className="alignLeft">Transactions</p> <p className="alignRight">{this.state.block.nTx}</p><hr className="columnRuler"/></Col>
              <Col><p className="alignLeft">Confirmations</p> <p className="alignRight">{this.state.block.confirmations}</p><hr className="columnRuler"/></Col>
              <Col><p className="alignLeft">Nonce</p> <p className="alignRight">{this.state.block.nonce}</p><hr className="columnRuler"/></Col>
            </Row>
            <Row>
              <Col><p className="alignLeft">Size</p> <p className="alignRight">{this.state.block.size}</p><hr className="columnRuler"/></Col>
              <Col><p className="alignLeft">Weight</p> <p className="alignRight">{this.state.block.weight}</p><hr className="columnRuler"/></Col>
              <Col><p className="alignLeft">Bits</p> <p className="alignRight">{this.state.block.bits}</p><hr className="columnRuler"/></Col>
            </Row>
          </Container>
          <h3 className="text-black my-4">Transactions </h3>
          <Alert variant="dark">
            <div className="alignLeft">
              Net Exchanged This Block
            </div>
            <div className="alignRight">
              {this.state.transactionsLoading ? 
              <div className="centerSpinner"><Spinner animation="border" role="status" size="sm"></Spinner></div> : 
              <><>
                {this.state.transactions.reduce( 
                  function(x, y) { 
                    return x + y.vout.reduce( 
                      function(a, b){ return a + b.value; }, 0 );
                  }, 0
                )}
              </> VTC</> 
              } 
            </div>
            <br/>
          </Alert>
          {this.state.transactionsLoading ? <div className="centerSpinner"><Spinner animation="border" role="status"></Spinner></div> : <></> }
          {this.state.transactions.map(tx => (
            <div key={tx.txid}>
            <Transaction tx={tx}/>
            <br/>
            </div>
          ))}
        </div>
      </main>
      );
      };
}