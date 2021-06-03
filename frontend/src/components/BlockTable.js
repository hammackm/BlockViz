import React, { Component } from 'react';
import {Table, Button, Spinner} from 'react-bootstrap';
import {BlockHeightOverlay} from './index'
import { Link } from "react-router-dom";
import axios from "axios";
import './style/BlockTable.scss'

export default class BlockTable extends Component {
    constructor(props) {
      super(props);
      this.state = {
        blocksWanted: 25,
        blockList: [],
        loading: true
      }
    }


    componentDidMount() {
      this.getBlocks(this.state.blocksWanted);
    }
  
    getBlocks = () => {
      axios
      .get("/recent/" + this.state.blocksWanted)
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

  render = () => {

        return (
          <main className="container">
            <h2 className="text-black my-4">Most Recent Vertcoin Blocks</h2>
            <div className="block table">
              <Table striped bordered hover variant="dark">
                <thead>
                  <tr>
                    <th>Block Height <BlockHeightOverlay/></th>
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