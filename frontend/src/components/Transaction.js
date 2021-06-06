import React, { Component } from 'react';
import axios from "axios";
import { Card, Container, Col, Row, Accordion, Button, useAccordionToggle} from 'react-bootstrap';
import { Link } from "react-router-dom";
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
    
                    let newtxidToVinAddressAmountMap = {...this.state.txidToVinAddressAmountMap, [txid] : { 
                        'address': txidAddress,
                        'amount': txidAmount,
                    }}
    
                    this.setState({txidToVinAddressAmountMap: newtxidToVinAddressAmountMap })
                })
                .catch((err) => console.log(err));
        });

        
    
      }

  render = () => {
    
    return (
        <Accordion>
            <Card border="dark">
                <Card.Header>
                    <Link to={'/transaction/'+this.props.tx.txid} variant='secondary'>
                        <div className="alignLeft">{this.props.tx.txid}</div>
                    </Link>
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
                            {[...Array(Math.max(this.props.tx.vin.length, this.props.tx.vout.length))].map((e, indx) => (
                                <div key={e}>
                                    <Row>
                                        <Col xs={4}>
                                            <div> {/* Im sorry in advance. Frontend is not my strong suit—js and functional programming is not my strong suit*/}
                                                <p className="alignLeftNotStrong">
                                                    {this.props.tx.vin[indx] ? 
                                                    <>{this.props.tx.vin[indx].coinbase ? 
                                                        <>New Coins + Fees</> : 
                                                        this.state.txidToVinAddressAmountMap[this.props.tx.vin[indx].txid] ? 
                                                            this.state.txidToVinAddressAmountMap[this.props.tx.vin[indx].txid].address :
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
                                                    {this.props.tx.vin[indx] ? 
                                                    <>{this.props.tx.vin[indx].coinbase ? 
                                                        <>New Coins + Fees</> : 
                                                        this.state.txidToVinAddressAmountMap[this.props.tx.vin[indx].txid] ? 
                                                            this.state.txidToVinAddressAmountMap[this.props.tx.vin[indx].txid].amount :
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
                                                    {this.props.tx.vout[indx] ? 
                                                    <>{this.props.tx.vout[indx].scriptPubKey.addresses ? 
                                                        this.props.tx.vout[indx].scriptPubKey.addresses.map(addr => (addr)) : 
                                                        <>Not Available</>}
                                                    </> : 
                                                    <></>}
                                                </p> 
                                            </div>
                                        </Col>
                                        <Col xs={2}>
                                            <p className="alignRight">
                                                {this.props.tx.vout[indx] ? 
                                                <>{this.props.tx.vout[indx].value} VTC</> : 
                                                <></>}
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