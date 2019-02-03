import React from "react";
import "./searchbar.css";

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
    width: "70%"
  }
};

export default class SearchBar extends React.Component {
  state = {
    searchQuery: this.props.match.params.query || "",
    className: this.props.match.params.query
      ? "search-text search-text-focus"
      : "search-text"
  };

  handleKeyPress = e => {
    if (e.key === "Enter") {
      this.props.history.push("/search/" + encodeURI(this.state.searchQuery));
    }
  };

  onFocus = () => {
    this.setState({ className: "search-text search-text-focus" });
  };

  onBlur = () => {
    if (this.state.searchQuery.length === 0)
      this.setState({ className: "search-text" });
    else this.setState({ className: "search-text search-text-focus" });
  };

  render() {
    return (
      <div style={styles.searchDiv}>
        <input
          type="search"
          name="q"
          value={this.state.searchQuery}
          onFocus={this.onFocus}
          onBlur={this.onBlur}
          onKeyPress={this.handleKeyPress}
          onChange={e => {
            this.setState({ searchQuery: e.target.value });
          }}
          className={this.state.className}
          placeholder="Search..."
        />
      </div>
    );
  }
}
