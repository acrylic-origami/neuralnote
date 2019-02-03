import React from "react";
import { Link } from "react-router-dom";

import "./searchView.css";

const styles = {
  entityCard: {
    width: "40%",
    display: "inline-block",
    padding: 20,
    margin: 10,
    borderRadius: 5
  },
  entityTitle: {
    background: "linear-gradient(90deg, #e66465, #9198e5)",
    color: "white",
    display: "inline-block"
  }
};

export default class SearchView extends React.Component {
  state = {
    entities: [
      {
        name: "bagel",
        results: [
          { docName: "Document 1", content: "I just had a bagel today..." },
          { docName: "Document 2", content: "I love bagels!!!" }
        ]
      },
      {
        name: "bread",
        results: [
          { docName: "Document 3", content: "My favorite bread recipe..." },
          { docName: "Document 1", content: "Bagels are a kind of bread" }
        ]
      }
    ]
  };

  render() {
    return (
      <div style={{ flexGrow: 1, overflow: "auto", padding: 20 }}>
        <h1>Results for: {this.props.match.params.query}</h1>
        {this.state.entities &&
          this.state.entities.map((entity, key) => {
            return (
              <Link
                key={key}
                to={"/entity/" + encodeURI(entity.name)}
                style={{ textDecoration: "none", color: "black" }}
              >
                <div className="searchResultCard" style={styles.entityCard}>
                  <div style={styles.entityTitle}>
                    <span>{entity.name}</span>
                  </div>
                </div>
              </Link>
            );
          })}
      </div>
    );
  }
}
