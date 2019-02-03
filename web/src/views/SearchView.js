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
    display: "inline-block",
    padding: 5,
    paddingLeft: 10,
    paddingRight: 10,
    borderRadius: 3
  },
  entityCardDocument: {
    textTransform: "uppercase",
    color: "#ABABA7",
    marginTop: 15,
    marginBottom: 5
  },
  entityCardContent: {
    fontWeight: 600,
    fontSize: 22,
    marginTop: 0
  }
};

export default class SearchView extends React.Component {
  state = {
    entities: [
      {
        name: "problems",
        results: [
          {
            docName: "Document 1",
            content: "Solving problems that are multi faceted..."
          },
          {
            docName: "Document 3",
            content: "Software is also a tough problem to solve"
          }
        ]
      },
      {
        name: "multi-faceted problems",
        results: [
          {
            docName: "Document 3",
            content: "politics it would even be a tough enough problem..."
          },
          {
            docName: "Ramblings",
            content:
              "tackle the problem of localization and you distribute your risk"
          }
        ]
      },
      {
        name: "business",
        results: [
          {
            docName: "Ramblings",
            content: "trying to build a MONOPOLY, then you do not need..."
          },
          {
            docName: "Document 1",
            content: "this is why I like business or design"
          }
        ]
      },
      {
        name: "design",
        results: [
          {
            docName: "Document 1",
            content: "this is why I like business or design"
          },
          {
            docName: "Document 2",
            content:
              "I sometimes struggle with the very personal I would put a piece of artwork"
          }
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
                    <span style={{ fontWeight: 700 }}>
                      &nbsp;{entity.name}&nbsp;
                    </span>
                  </div>
                  {entity.results.map((result, key) => {
                    return (
                      <div key={key}>
                        <h4 style={styles.entityCardDocument}>
                          {result.docName}
                        </h4>
                        <p style={styles.entityCardContent}>{result.content}</p>
                      </div>
                    );
                  })}
                </div>
              </Link>
            );
          })}
      </div>
    );
  }
}
