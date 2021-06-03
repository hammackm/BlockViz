import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { TitleBar, Footer, BlockTable, About, BlockDetails, Analytics} from "./components";
import axios from "axios";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      blockSelected: {'height': 0},
    };
  }

  getBlockByHeight = (height) => {
    axios
    .get("/height/" + height)
    .then((res) => this.setState({blockSelected: res.data}))
    .catch((err) => console.log(err));
  };
  

  render() {
    return (
      <div className="App">
        <Router>
          <TitleBar />
          <Switch>
            <Route path="/" exact component={() => <BlockTable blocks={this.state.blockList}/>} />
            <Route path="/about" exact component={() => <About />} />
            <Route path={"/block"} exact component={() => <BlockDetails block={this.state.blockSelected}/>} />
            <Route path="/analytics" exact component={() => <Analytics />} />
          </Switch>
          <Footer />
        </Router>
      </div>
    );
  }
}



export default App;