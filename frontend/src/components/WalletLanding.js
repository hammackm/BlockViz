import React, { Component } from 'react';
import {Button, Spinner, Form, Col, Table} from 'react-bootstrap';
import { Link } from "react-router-dom";
import axios from "axios";
//import './style/TransactionTable.scss'

export default class WalletLanding extends Component {
    constructor(props) {
      super(props);
      this.state = {
        walletFormData: '',
      }
    }

    componentDidMount() {
      
    }

    onFormChange = (event) => {
      event.preventDefault()
      this.setState({
        walletFormData: event.target.value
      })
    }


  render = () => {

        return (
          <main className="container">
            <h2 className="text-black my-4">View Vertcoin Wallets/Addresses</h2>
            <Form>
              <Form.Row className="align-items-center">
                <Col xs="4">
                  <Form.Control
                    className="mb-2"
                    type="text"
                    onChange={this.onFormChange}
                    name="block"
                    id="inlineFormInput"
                    placeholder="Wallet Address"
                  />
                </Col>
                <Col xs="auto">
                <Link to={'/wallet/'+this.state.walletFormData} variant='secondary'> {/* Not Proper HTML */}
                  <Button type="submit" className="mb-2" variant="outline-dark">
                    Go
                  </Button>
                </Link>
                </Col>
              </Form.Row>
              <Form.Row>
                <Col>
                  <Form.Text id="blockdHelpInline" muted>
                    Enter the Wallet Address to view more details.
                  </Form.Text>
                </Col>
              </Form.Row>
            </Form>
            <br/>
            <h3 className="text-black my-4">Known/Popular Vertcoin Wallets</h3>
            <div className="block table">
              <Table striped bordered hover variant="dark">
                <thead>
                  <tr>
                    <th>Wallet Address</th>
                    <th>Received</th>
                    <th>Sent</th>
                    <th>Balance</th>
                    <th>Owner/Affliation</th>
                  </tr>
                </thead>
                <tbody>
                </tbody>
              </Table>
            </div>
        </main>
          
        );
      };
}