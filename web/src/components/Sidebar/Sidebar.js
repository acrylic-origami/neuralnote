import React from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";

const styles = {
  sidebar: {
    fontFamily: ["Helvetica Neue", "Helvetica", "Arial", "sans-serif"],
    background: "#F9F9F7",
    padding: 10,
    overflow: "auto"
  },
  logoTitle: {
    fontSize: 30
  },
  logoImg: {
    width: 80,
    position: "relative",
    top: 0,
    right: 0
  },
  documents: {
    color: "#ABABA7",
    fontSize: 18
  },
  docBullet: {
    color: "#ABABA7"
  },
  addButtonDiv: {
    position: "absolute",
    bottom: 0,
    left: 0,
    margin: 20
  },
  addButton: {
    display: "block",
    width: 50,
    height: 50,
    lineHeight: 0,
    borderRadius: "50%",
    backgroundColor: "#7942FB",
    color: "white",
    textAlign: "center",
    fontSize: 20,
    fontWeight: "bold",
    outline: "none"
  }
};

export default class Sidebar extends React.Component {
  render() {
    return (
      <div style={{ ...styles.sidebar, ...this.props.style }}>
        <div>
          <h2 style={styles.logoTitle}>Neural Notes</h2>
          {/* <img
            src={require("../../assets/img/flamingo.png")}
            alt="logo"
            style={styles.logoImg}
          /> */}
        </div>

        <h3 style={styles.documents}>DOCUMENTS</h3>
        {this.props.documents &&
          this.props.documents.map((documentName, i) => {
            return (
              <Link
                key={i}
                to={"/document/" + encodeURI(documentName)}
                style={{ textDecoration: "none", color: "black" }}
              >
                <p>
                  <span style={styles.docBullet}>►</span> {documentName}
                </p>
              </Link>
            );
          })}
        <div style={styles.addButtonDiv}>
          <button style={styles.addButton} onClick={this.props.onAdd}>
            +
          </button>
        </div>
      </div>
    );
  }
}

Sidebar.propTypes = {
  style: PropTypes.object,
  documents: PropTypes.array.isRequired,
  onAdd: PropTypes.func
};
