import React, { Component } from 'react';
import axios from "axios";
import { Col, Container, Row, Card } from 'react-bootstrap';
import './style/TransactionDetails.scss'

export default class TransactionDetails extends Component {
  constructor(props) {
    super(props);
    this.state = {
      transaction: {},
      txidToVinAddressAmountMap: {},
    };
  }

  getTransactionMapping(tx) {

    tx.vin
        .filter(vin => !vin.coinbase)
        .forEach(e => {

            axios
                .get(`/transaction/${e.txid}`)
                .then((res) => {
                    let transaction = res.data
                    let txid = res.data.txid
                    let txidAddress = transaction.vout[e.vout].scriptPubKey.addresses[0]
                    let txidAmount = transaction.vout[e.vout].value
    
                    let newtxidToVinAddressAmountMap = {...this.state.txidToVinAddressAmountMap, [txid] : { 
                        'address': txidAddress,
                        'amount': txidAmount,
                    }}
    
                    this.setState({txidToVinAddressAmountMap: newtxidToVinAddressAmountMap })
                })
                .catch((err) => console.log(err));
        });
  }

  componentDidMount() {

    axios
    .get(`/transaction/${this.props.match.params.txid}`)
    .then((res) => this.setState({
      transaction: res.data,
    }, () => this.getTransactionMapping(this.state.transaction)))
    .catch((err) => console.log(err));

  }

  render = () => {

    console.log("render: ", this.state.transaction)

    if(!this.state.transaction.vout) {
        return <div/>
    }

    return (
      <main className="container">
        <h2 className="text-black my-4">Transaction: {this.props.match.params.txid}</h2>
        <div className="blockdetails">
          <Container>
            <Row>
              <Col><div><p className="alignLeft">Hash</p> <p className="alignRight">{this.state.transaction.hash}</p></div><hr className="columnRuler"/></Col>
            </Row>
            <Row>
              <Col><div><p className="alignLeft">Block Hash</p> <p className="alignRight">{this.state.transaction.blockhash}</p></div><hr className="columnRuler"/></Col>
            </Row>
            <hr className="bodyRuler"/>
            <Row>
              <Col><p className="alignLeft">Confirmations</p> <p className="alignRight">{this.state.transaction.confirmations}</p><hr className="columnRuler"/></Col>
              <Col><p className="alignLeft">Version</p> <p className="alignRight">{this.state.transaction.version}</p><hr className="columnRuler"/></Col>
            </Row>
            <Row>
              <Col><p className="alignLeft">Timestamp</p> <p className="alignRight">{this.state.transaction.time}</p><hr className="columnRuler"/></Col>
              <Col><p className="alignLeft">Block Time</p> <p className="alignRight">{this.state.transaction.blocktime}</p><hr className="columnRuler"/></Col>
            </Row>
            <hr className="bodyRuler"/>
            <Row>
              <Col><p className="alignLeft">Fee</p> <p className="alignRight">{}</p><hr className="columnRuler"/></Col>
              <Col><p className="alignLeft">Fee Rate</p> <p className="alignRight">{}</p><hr className="columnRuler"/></Col>
              <Col><p className="alignLeft">Nonce</p> <p className="alignRight">{}</p><hr className="columnRuler"/></Col>
            </Row>
            <Row>
              <Col><p className="alignLeft">Size</p> <p className="alignRight">{this.state.transaction.size}</p><hr className="columnRuler"/></Col>
              <Col><p className="alignLeft">VSize</p> <p className="alignRight">{this.state.transaction.vsize}</p><hr className="columnRuler"/></Col>
              <Col><p className="alignLeft">Weight</p> <p className="alignRight">{this.state.transaction.weight}</p><hr className="columnRuler"/></Col>
            </Row>
          </Container>
          <br/>
            <Card border="dark">
                <Card.Body>
                    <Container>
                        <Row>
                            <Col className="exTx">
                            <div className="alignLeft">Net Exchanged This Transaction</div> 
                            <div className="alignRight">
                                {this.state.transaction.vout.reduce( function(a, b){ return a + b.value; }, 0)} VTC
                            </div>
                            </Col>
                        </Row>
                        <br/>
                        <Row>
                            <Col xs={6}>
                                <div>
                                    <p className="alignLeft">Input Address </p>
                                    <p className="alignRight"><b>Sent</b></p>
                                </div>
                                <hr className="columnRuler"/>
                            </Col>
                            <Col xs={6}>
                                <div>
                                    <p className="alignLeft">Output Address</p> 
                                    <p className="alignRight"><b>Received</b></p>
                                </div>
                                <hr className="columnRuler"/>
                            </Col>
                        </Row>
                        {[...Array(Math.max(this.state.transaction.vin.length, this.state.transaction.vout.length))].map((e, indx) => (
                            <div key={e}>
                                <Row>
                                    <Col xs={4}>
                                        <div> {/* Im sorry in advance. Frontend is not my strong suit—js and functional programming is not my strong suit*/}
                                            <p className="alignLeftNotStrong">
                                                {this.state.transaction.vin[indx] ? 
                                                <>{this.state.transaction.vin[indx].coinbase ? 
                                                    <>New Coins + Fees</> : 
                                                    this.state.txidToVinAddressAmountMap[this.state.transaction.vin[indx].txid] ? 
                                                        this.state.txidToVinAddressAmountMap[this.state.transaction.vin[indx].txid].address :
                                                        <></>
                                                    }
                                                </> : 
                                                <></>}
                                            </p>
                                        </div>
                                    </Col>
                                    <Col xs={2}>
                                        <div> {/* Im sorry in advance. Frontend is not my strong suit—js and functional programming is not my strong suit*/}
                                            <p className="alignRight">
                                                {this.state.transaction.vin[indx] ? 
                                                <>{this.state.transaction.vin[indx].coinbase ? 
                                                    <>New Coins + Fees</> : 
                                                    this.state.txidToVinAddressAmountMap[this.state.transaction.vin[indx].txid] ? 
                                                        this.state.txidToVinAddressAmountMap[this.state.transaction.vin[indx].txid].amount :
                                                        <></>
                                                    }
                                                </> : 
                                                <></>} 
                                            </p>
                                        </div>
                                    </Col>
                                    <Col xs={4}>
                                        <div>
                                            <p className="alignLeftNotStrong">
                                                {this.state.transaction.vout[indx] ? 
                                                <>{this.state.transaction.vout[indx].scriptPubKey.addresses ? 
                                                    this.state.transaction.vout[indx].scriptPubKey.addresses.map(addr => (addr)) : 
                                                    <>Not Available</>}
                                                </> : 
                                                <></>}
                                            </p> 
                                        </div>
                                    </Col>
                                    <Col xs={2}>
                                        <p className="alignRight">
                                            {this.state.transaction.vout[indx] ? 
                                            <>{this.state.transaction.vout[indx].value} VTC</> : 
                                            <></>}
                                        </p>
                                    </Col>
                                </Row>
                            </div>
                        ))}
                        </Container>
                </Card.Body>
            </Card>

        </div>
      </main>
      );
      };
}