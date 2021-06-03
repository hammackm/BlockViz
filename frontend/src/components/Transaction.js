import React, { Component } from 'react';
import { Card, CardColumns, Container, Col, Row } from 'react-bootstrap';
import './style/Transaction.scss'

export default class Transaction extends Component {

  render = () => {
      console.log(this.props.tx)
    return (
      <Card>
          <Card.Header><b>Transaction:</b> {this.props.tx.txid}</Card.Header>
          <Card.Body>
            <Container>
                <Row>
                    <Col>
                    <p className="alignLeft">Net Exchanged</p> 
                    <p className="alignRight">
                        {this.props.tx.vout.reduce( function(a, b){ return a + b.value; }, 0)}
                    </p>
                    <hr className="columnRuler"/>
                    </Col>
                </Row>
                {this.props.tx.vout.map(v => (
                        <>
                            <Row>
                                <Col>
                                    <div>
                                        <p className="alignLeft">Amount </p>
                                        <p className="alignRight">
                                            {v.value}
                                        </p>
                                    </div>
                                    <hr className="columnRuler"/>
                                </Col>
                                <Col>
                                    <div>
                                        <p className="alignLeft">Receiving Addr </p> 
                                        <p className="alignRight">
                                            {v.scriptPubKey.addresses ? v.scriptPubKey.addresses.map(addr => (addr)) : <></>}
                                        </p>
                                    </div>
                                    <hr className="columnRuler"/>
                                </Col>
                            </Row>
                        </>
                    ))}
                </Container>
          </Card.Body>
      </Card>
      );
      };
}