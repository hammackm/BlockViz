import React, { Component } from 'react';
import {Table, Button, Spinner, Form, Col} from 'react-bootstrap';
import { Link } from "react-router-dom";
import axios from "axios";
import './style/BlockLanding.scss'

export default class BlockLandin extends Component {
    constructor(props) {
      super(props);
      this.state = {
        blocksWanted: 10,
        blockList: [],
        loading: true,
        blockFormData: '',
      }
    }


    componentDidMount() {
      this.getBlocks(this.state.blocksWanted);
    }
  
    getBlocks = () => {
      axios
      .get("/recent/block/" + this.state.blocksWanted)
      .then((res) => this.setState({
        blockList: res.data,
        loading: false,
      }))
      .catch((err) => console.log(err));
    };

    handleShowMoreClick = () => {
      this.setState({
        blocksWanted: this.state.blocksWanted+25,
        loading: true
      }, 
        () => {this.getBlocks(this.state.blocksWanted)}
        )
    }

    onFormChange = (event) => {
      event.preventDefault()

      if(event.target.value.length === 64) {
        axios
        .get("/blockhash/" + event.target.value)
        .then((res) => this.setState({
          blockFormData: res.data.height
        }))
        .catch((err) => console.log(err));
      }
      else {
        this.setState({
          blockFormData: event.target.value
        })
      }
    }


  render = () => {

        return (
          <main className="container">
            <h2 className="text-black my-4">Vertcoin Blocks</h2>
            <Form>
              <Form.Row className="align-items-center">
                <Col xs="4">
                  <Form.Control
                    className="mb-2"
                    type="text"
                    onChange={this.onFormChange}
                    name="block"
                    id="inlineFormInput"
                    placeholder="Block Height or Hash"
                  />
                </Col>
                <Col xs="auto">
                <Link to={'/block/'+this.state.blockFormData} variant='secondary'> {/* Not Proper HTML */}
                  <Button type="submit" className="mb-2" variant="outline-dark">
                    Go
                  </Button>
                </Link>
                </Col>
              </Form.Row>
              <Form.Row>
                <Col>
                  <Form.Text id="blockdHelpInline" muted>
                    Enter Block Height or Hash to view more details and transactions.
                  </Form.Text>
                </Col>
              </Form.Row>
            </Form>
            <h3 className="text-black my-4">Latest Blocks</h3>
            <div className="block table">
              <Table striped bordered hover variant="dark">
                <thead>
                  <tr>
                    <th>Block Height</th>
                    <th>Timestamp</th>
                    <th># Transactions</th>
                    <th># Confirmations</th>
                    <th>Size</th>
                    <th>Difficulty</th>
                  </tr>
                </thead>
                <tbody>
                  {this.state.blockList.map(block => (
                    <tr key={block.height}>
                        <td><Link to={'/block/'+block.height} variant='secondary'>{block.height}</Link></td>
                        <td>{block.time}</td>
                        <td>{block.nTx}</td>
                        <td>{block.confirmations}</td>
                        <td>{block.size}</td>
                        <td>{block.difficulty}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>
            {this.state.loading ? <div className="centerSpinner"><Spinner animation="border" role="status"></Spinner></div> : <div /> }
            <div className="text-center"><Button  onClick={this.handleShowMoreClick} variant="outline-dark">———— Show More ————</Button></div>
        </main>
          
        );
      };
}