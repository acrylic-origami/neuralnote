import React from "react";
import { IoIosSearch } from "react-icons/io";

const styles = {
  searchDiv: {
    width: "100%",
    borderBottom: "1px solid black",
    padding: 20
  },
  searchIcon: {
    fontSize: 30,
    float: "left",
    display: "inline-block"
  },
  searchInput: {
    padding: 8,
    display: "inline-block",
    border: "none",
    width: "70%",
    transition: "width 0.4s ease-in-out"
  }
};

export default class SearchBar extends React.Component {
  state = {
    searchQuery: ""
  };

  submitSearch = () => {
    this.props.history.push("/search/" + encodeURI(this.state.searchQuery));
  };

  render() {
    return (
      <div style={{ ...styles.searchDiv }}>
        <span style={styles.searchIcon}>
          <IoIosSearch />
        </span>
        <input
          style={styles.searchInput}
          value={this.state.searchQuery}
          onChange={e => {
            this.setState({ searchQuery: e.target.value });
          }}
        />
        <button style={{ display: "inline-block" }} onClick={this.submitSearch}>
          Enter
        </button>
      </div>
    );
  }
}
