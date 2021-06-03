import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { TitleBar, Footer, BlockTable, About, BlockDetails, Analytics, LiveChain} from "./components";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      blockSelected: {'height': 0},
    };
  }

  blockSelectedCallback = (blockSelectedBelow) => {
    console.log('callback ran: ' + blockSelectedBelow.height)
    this.setState({blockSelected: blockSelectedBelow})
    console.log('State after set state: ')
    console.log(this.state)
  }
  

  render() {
    return (
      <div className="App">
        <Router>
          <TitleBar />
          <Switch>
            <Route path="/" exact component={() => <BlockTable blocks={this.state.blockList}/>} />
            <Route path="/about" exact component={() => <About />} />
            <Route path="/block/:blockHeight" component={BlockDetails} />
            <Route path="/analytics" exact component={() => <Analytics />} />
            <Route path="/livechain" exact component={() => <LiveChain />} />
          </Switch>
          <Footer />
        </Router>
      </div>
    );
  }
}



export default App;