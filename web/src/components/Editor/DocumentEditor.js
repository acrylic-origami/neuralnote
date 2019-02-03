import React from "react";
import { Editor } from "react-draft-wysiwyg";
import "react-draft-wysiwyg/dist/react-draft-wysiwyg.css";

export default class DocumentEditor extends React.Component {
  state = {
    editorState: ""
  };

  render() {
    return (
      <div style={{ flex: 1 }}>
        <Editor
          toolbarClassName="demo-toolbar-absolute"
          wrapperClassName="demo-wrapper"
          editorClassName="demo-editor"
          toolbarOnFocus
          wrapperStyle={{ height: "100%" }}
          toolbar={{
            options: ["inline", "fontSize", "fontFamily", "list", "history"],
            inline: {
              options: [
                "bold",
                "italic",
                "underline",
                "strikethrough",
                "monospace"
              ],
              bold: { className: "bordered-option-classname" },
              italic: { className: "bordered-option-classname" },
              underline: { className: "bordered-option-classname" },
              strikethrough: { className: "bordered-option-classname" },
              code: { className: "bordered-option-classname" }
            },
            blockType: {
              className: "bordered-option-classname"
            },
            fontSize: {
              className: "bordered-option-classname"
            },
            fontFamily: {
              className: "bordered-option-classname"
            }
          }}
        />
      </div>
    );
  }
}
