import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import { Sidebar } from "./components/Sidebar";
import { DocumentEditor } from "./components/Editor";
import { SearchView, EntityView } from "./views";
import SearchBar from "./components/SearchBar/SearchBar";
import EntityBar from "./components/EntityBar/EntityBar";

class App extends Component {
  state = {
    documentTitles: ["Document 1", "Document 2", "Document 3", "Ramblings"]
  };

  onAdd = () => {
    let oldTitles = this.state.documentTitles;
    oldTitles.push("New Document");
    this.setState({
      documentTitles: oldTitles
    });
  };

  render() {
    return (
      <Router>
        <div style={{ display: "flex", height: "100%" }}>
          <Sidebar
            style={{ flex: 1 }}
            documentTitles={this.state.documentTitles}
            onAdd={this.onAdd}
          />
          <div
            style={{
              flex: 3,
              height: "100%",
              flexDirection: "column"
            }}
          >
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                height: "100%"
              }}
            >
              <Switch>
                <Route path="/entity/:entityName" component={EntityBar} />
                <Route path="/search/:query" component={SearchBar} />
                <Route path="/" component={SearchBar} />
              </Switch>

              <div style={{ flexGrow: 1, display: "flex" }}>
                <Route path="/" exact component={DocumentEditor} />
                <Route path="/search/:query" component={SearchView} />
                <Route path="/entity/:entityName" component={EntityView} />
              </div>
            </div>
          </div>
        </div>
      </Router>
    );
  }
}

export default App;
