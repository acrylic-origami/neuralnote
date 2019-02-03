import React from "react";
import { Link } from "react-router-dom";

import "./searchView.css";

const styles = {
  documentCard: {
    width: "40%",
    display: "inline-block",
    padding: 0,
    margin: 10,
    borderRadius: 5,
    position: "relative"
  },
  docTitleDiv: {
    borderBottom: "1px solid grey",
    borderLeft: "1px solid grey",
    borderBottomLeftRadius: 10,
    display: "inline-block",
    position: "absolute",
    top: 0,
    right: 0,
    padding: "0 10px",
    paddingTop: 4
  },
  documentCardTitle: {
    textTransform: "uppercase",
    color: "#ABABA7",
    marginTop: 0,
    marginBottom: 5
  },
  documentCardContent: {
    fontWeight: 600,
    fontSize: 22,
    padding: 20,
    paddingTop: 30,
    marginTop: 0
  }
};

export default class SearchView extends React.Component {
  state = {
    results: [
      { docName: "Document 3", content: "My favorite bread recipe..." },
      { docName: "Document 1", content: "Bagels are a kind of bread" }
    ]
  };

  render() {
    return (
      <div style={{ flexGrow: 1, overflow: "auto", padding: 20 }}>
        <h1>Results for: {this.props.match.params.entityName}</h1>
        {this.state.results &&
          this.state.results.map((result, key) => {
            return (
              <Link
                key={key}
                to={"/document/" + encodeURI(result.docName)}
                style={{ textDecoration: "none", color: "black" }}
              >
                <div className="searchResultCard" style={styles.documentCard}>
                  <div style={styles.docTitleDiv}>
                    <h4 style={styles.documentCardTitle}>{result.docName}</h4>
                  </div>
                  <p style={styles.documentCardContent}>{result.content}</p>
                </div>
              </Link>
            );
          })}
      </div>
    );
  }
}
