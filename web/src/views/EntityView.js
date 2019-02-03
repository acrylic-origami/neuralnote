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
    results: {
      problems: [
        {
          docName: "Document 1",
          content: "Solving problems that are multi faceted..."
        },
        {
          docName: "Document 3",
          content: "Software is also a tough problem to solve"
        }
      ],
      "multi-faceted problems": [
        {
          docName: "Document 3",
          content: "politics it would even be a tough enough problem..."
        },
        {
          docName: "Ramblings",
          content:
            "tackle the problem of localization and you distribute your risk"
        }
      ],
      business: [
        {
          docName: "Ramblings",
          content: "trying to build a MONOPOLY, then you do not need..."
        },
        {
          docName: "Document 1",
          content: "this is why I like business or design"
        }
      ],
      design: [
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
  };

  render() {
    let currentEntity = decodeURI(this.props.match.params.entityName);
    let entityData = this.state.results[currentEntity];

    return (
      <div
        style={{
          flexGrow: 1,
          overflow: "auto",
          padding: 20,
          minHeight: 0
        }}
      >
        {entityData ? (
          entityData.map((document, key) => {
            return (
              <Link
                key={key}
                to={"/document/" + encodeURI(document.docName)}
                style={{ textDecoration: "none", color: "black" }}
              >
                <div className="searchResultCard" style={styles.documentCard}>
                  <div style={styles.docTitleDiv}>
                    <h4 style={styles.documentCardTitle}>{document.docName}</h4>
                  </div>
                  <p style={styles.documentCardContent}>{document.content}</p>
                </div>
              </Link>
            );
          })
        ) : (
          <h2>No Results Found.</h2>
        )}
      </div>
    );
  }
}
