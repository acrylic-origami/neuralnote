import React from "react";
import { Link } from "react-router-dom";
import { IoMdArrowBack } from "react-icons/io";

const styles = {
  entityDiv: {
    width: "100%",
    borderBottom: "1px solid black",
    padding: 20
  },
  backIcon: {
    fontSize: 35,
    float: "left",
    display: "inline-block"
  },
  entityTitle: {
    background: "linear-gradient(90deg, #e66465, #9198e5)",
    color: "white",
    display: "inline-block",
    padding: 5,
    paddingLeft: 10,
    paddingRight: 10,
    borderRadius: 3,
    marginLeft: 20,
    marginTop: 5
  }
};

export default class EntityBar extends React.Component {
  goBack = () => {
    this.props.history.goBack();
  };

  render() {
    return (
      <div style={styles.entityDiv}>
        <Link to="" onClick={this.goBack} style={{ color: "#747474" }}>
          <span style={styles.backIcon}>
            <IoMdArrowBack />
          </span>
        </Link>
        <div style={styles.entityTitle}>
          <span>{this.props.match.params.entityName}</span>
        </div>
      </div>
    );
  }
}
