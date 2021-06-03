import React, { Component } from 'react';
import {Table, Button} from 'react-bootstrap';
import {HeaderOverlay} from './index'
import axios from "axios";

const headerInfo = {
  'Height': {
    'headText': 'Block Height',
    'bodyText': 'Height of the Vertcoin blockchain',
  }
}

export default class BlockTable extends Component {
    constructor(props) {
      super(props);
      this.state = {
        blocksWanted: 25,
        blockList: [],
      }
    }


    componentDidMount() {
      this.getBlocks(this.state.blocksWanted);
    }
  
    getBlocks = (blocksWanted) => {
      axios
      .get("/recent/" + blocksWanted)
      .then((res) => this.setState({blockList: res.data}))
      .catch((err) => console.log(err));
    };

    handleShowMoreClick = () => {
      this.setState({blocksWanted: this.state.blocksWanted+25})
      this.getBlocks(this.state.blocksWanted)
    }

  render = () => {

        return (
          <main className="container">
            <h2 className="text-black my-4">Most Recent Vertcoin Blocks</h2>
            <div className="block table">
              <Table striped bordered hover variant="dark">
                <thead>
                  <tr>
                    <th>Block Height <HeaderOverlay {...headerInfo.height}/></th>
                    <th>Timestamp</th>
                    <th># Transactions</th>
                    <th># Confirmations</th>
                    <th>Size</th>
                    <th>Difficulty</th>
                  </tr>
                </thead>
                <tbody>
                  {this.state.blockList.map(block => (
                    <tr>
                        <a href={"/block"}><td>{block.height}</td></a>
                        <td>{block.time}</td>
                        <td>{block.transactions}</td>
                        <td>{block.confirmations}</td>
                        <td>{block.size}</td>
                        <td>{block.difficulty}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>
            <div className="text-center"><Button  onClick={this.handleShowMoreClick} variant="outline-dark">———— Show More ————</Button></div>
            <div></div>
        </main>
          
        );
      };
}