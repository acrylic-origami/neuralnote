// import React from "react";

// import { Sidebar } from "../components/Sidebar";
// import { DocumentEditor } from "../components/Editor";
// import SearchBar from "../components/SearchBar/SearchBar";

// export default class DefaultView extends React.Component {
//   state = {
//     documentTitles: ["Document 1", "Document 2", "Document 3", "Ramblings"],
//     searchQuery: ""
//   };

//   onAdd = () => {
//     let oldTitles = this.state.documentTitles;
//     oldTitles.push("New Document");
//     this.setState({
//       documentTitles: oldTitles
//     });
//   };

//   submitSearch = () => {
//     this.props.history.push("search/" + encodeURI(this.state.searchQuery));
//   };

//   render() {
//     return (
//       <div style={{ display: "flex", height: "100%" }}>
//         <Sidebar
//           style={{ flex: 1 }}
//           documentTitles={this.state.documentTitles}
//           onAdd={this.onAdd}
//         />
//         <div
//           style={{
//             flex: 3,
//             height: "100%",
//             flexDirection: "column"
//           }}
//         >
//           <div
//             style={{
//               display: "flex",
//               flexDirection: "column",
//               height: "100%"
//             }}
//           >
//             <SearchBar />

//             <div style={{ flexGrow: 1, display: "flex" }}>
//               <DocumentEditor />
//             </div>
//           </div>
//         </div>
//       </div>
//     );
//   }
// }
