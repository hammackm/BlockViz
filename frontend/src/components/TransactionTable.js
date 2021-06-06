import React, { Component } from 'react';
import {Table, Button, Spinner, Form, Col} from 'react-bootstrap';
import {BlockHeightOverlay} from './index'
import { Link } from "react-router-dom";
import axios from "axios";
import './style/TransactionTable.scss'

export default class TransactionTable extends Component {
    constructor(props) {
      super(props);
      this.state = {
        transactionList: [],
        loading: true,
        transactionFormData: '',
      }
    }


    componentDidMount() {
      this.getMemPool();
    }
  
    getMemPool = () => {
      axios
      .get("/mempool/")
      .then((res) => this.setState({
        transactionList: res.data,
        loading: false,
      }))
      .catch((err) => console.log(err));
    };

    handleShowMoreClick = () => {
      this.setState({
        loading: true
      }, () => this.getMemPool()
        )
    }

    onFormChange = (event) => {
      event.preventDefault()
      this.setState({
        transactionFormData: event.target.value
      })
    }


  render = () => {

        return (
          <main className="container">
            <h2 className="text-black my-4">View Vertcoin Transactions</h2>
            <Form>
              <Form.Row className="align-items-center">
                <Col xs="4">
                  <Form.Control
                    className="mb-2"
                    type="text"
                    onChange={this.onFormChange}
                    name="block"
                    id="inlineFormInput"
                    placeholder="Transaction ID"
                  />
                </Col>
                <Col xs="auto">
                <Link to={'/transaction/'+this.state.transactionFormData} variant='secondary'> {/* Not Proper HTML */}
                  <Button type="submit" className="mb-2" variant="outline-dark">
                    Go
                  </Button>
                </Link>
                </Col>
              </Form.Row>
              <Form.Row>
                <Col>
                  <Form.Text id="blockdHelpInline" muted>
                    Enter Transaction ID to view more details.
                  </Form.Text>
                </Col>
              </Form.Row>
            </Form>
            <h3 className="text-black my-4">Unmined Vertcoin Transactions</h3>
            <div className="block table">
              <Table striped bordered hover variant="dark">
                <thead>
                  <tr>
                    <th>Transaction ID</th>
                  </tr>
                </thead>
                <tbody>
                  {this.state.transactionList.map(txid => (
                    <tr key={txid}>
                        <td><Link to={'/transaction/'+txid} variant='secondary'>{txid}</Link></td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>
            {this.state.loading ? <div className="centerSpinner"><Spinner animation="border" role="status"></Spinner></div> : <div /> }
            <div className="text-center"><Button  onClick={this.handleShowMoreClick} variant="outline-dark">———— Refresh Pool ————</Button></div>
        </main>
          
        );
      };
}