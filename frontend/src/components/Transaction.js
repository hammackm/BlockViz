import React, { Component } from 'react';
import axios from "axios";
import { Card, Container, Col, Row, Accordion, Button, useAccordionToggle } from 'react-bootstrap';
import './style/Transaction.scss'

function CustomToggle({ children, eventKey }) {
    const decoratedOnClick = useAccordionToggle("0");
  
    return (
        <Button  onClick={decoratedOnClick} variant="outline-dark" size="sm">{children}</Button>
    );
  }



export default class Transaction extends Component {
    constructor(props) {
        super(props);
        this.state = {
          txidToVinAddressAmountMap: {}
        };
      }

    componentDidMount() {

        let newtxidToVinAddressAmountMap = {}

        this.props.tx.vin
        .filter(vin => !vin.coinbase)
        .forEach(e => {
 
            axios
                .get(`/transaction/${e.txid}`)
                .then((res) => {
                    let transaction = res.data
                    let txid = res.data.txid
                    let txidAddress = transaction.vout[e.vout].scriptPubKey.addresses[0]
                    let txidAmount = transaction.vout[e.vout].value
    
                    newtxidToVinAddressAmountMap = {...newtxidToVinAddressAmountMap, [txid] : { 
                        'address': txidAddress,
                        'amount': txidAmount,
                    }}
    
                    
                })
                .catch((err) => console.log(err));
        });

        this.setState({txidToVinAddressAmountMap: newtxidToVinAddressAmountMap })
    
      }

  render = () => {
    
    console.log("render called")
    console.log(this.state.txidToVinAddressAmountMap)
    return (
        <Accordion>
            <Card border="dark">
                <Card.Header>
                    <div className="alignLeft">{this.props.tx.txid}</div>
                    <div className="alignRight"><CustomToggle>Details</CustomToggle></div>
                </Card.Header>
                <Accordion.Collapse eventKey="0">
                    <Card.Body>
                        <Container>
                            <Row>
                                <Col className="exTx">
                                <div className="alignLeft">Net Exchanged This Transaction</div> 
                                <div className="alignRight">
                                    {this.props.tx.vout.reduce( function(a, b){ return a + b.value; }, 0)} VTC
                                </div>
                                </Col>
                            </Row>
                            <br/>
                            <Row>
                                <Col xs={6}>
                                    <div>
                                        <p className="alignLeft">Input Transactions </p>
                                    </div>
                                    <hr className="columnRuler"/>
                                </Col>
                                <Col xs={4}>
                                    <div>
                                        <p className="alignLeft">Output Addresses </p> 
                                    </div>
                                    <hr className="columnRuler"/>
                                </Col>
                                <Col xs={2}>
                                    <p className="alignRight">
                                        <b>Vout Amount</b>
                                    </p>
                                    <hr className="columnRuler"/>
                                </Col>
                            </Row>
                            {[...Array(Math.max(this.props.tx.vin.length, this.props.tx.vout.length))].map((e, indx) => (
                                    <div key={e}>
                                        <Row>
                                            <Col xs={6}>
                                                <div>
                                                    <p className="alignLeftNotStrong">{this.props.tx.vin[indx] ? <>{this.props.tx.vin[indx].coinbase ? <>Coinbase</> : this.state.txidToVinAddressAmountMap[this.props.tx.vin[indx].txid]+"... vout: "+this.props.tx.vin[indx].vout}</> : <></>}</p>
                                                </div>
                                            </Col>
                                            <Col xs={4}>
                                                <div>
                                                    <p className="alignLeftNotStrong"> {this.props.tx.vout[indx] ? <>{this.props.tx.vout[indx].scriptPubKey.addresses ? this.props.tx.vout[indx].scriptPubKey.addresses.map(addr => (addr)) : <>Not Available</>}</> : <></>} </p> 
                                                </div>
                                            </Col>
                                            <Col xs={2}>
                                                <p className="alignRight">
                                                    {this.props.tx.vout[indx] ? <>{this.props.tx.vout[indx].value} VTC</> : <></>}
                                                </p>
                                            </Col>
                                        </Row>
                                    </div>
                                ))}
                            </Container>
                    </Card.Body>
                </Accordion.Collapse>
            </Card>
        </Accordion>
      );
      };
}