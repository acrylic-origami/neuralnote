import React from "react";
import { Editor } from "react-draft-wysiwyg";
import { stateToHTML } from "draft-js-export-html";
import draftToHtml from "draftjs-to-html";
import htmlToDraft from "html-to-draftjs";
import {
  EditorState,
  ContentState,
  convertFromHTML,
  convertFromRaw,
  convertToRaw
} from "draft-js";
import "react-draft-wysiwyg/dist/react-draft-wysiwyg.css";

export default class DocumentEditor extends React.Component {
  state = {
    editorState: EditorState.createEmpty(),
    searched: false,
    documents: {
      "Document 1":
        "Solving problems that are multi faceted this is why I like business or design because it is trying to shoot and solution tough factor space a lot of competing factors. But I also want that problem to move things forward in someway, it needs to be something that is moving Society forward.",
      "Document 2":
        "I like design because you were also trying to optimize and find a solution, but I sometimes struggle with the very personal I would put a piece of artwork. When someone does not like the aesthetic’s of something I have made or disagrees, I have difficulties when they do not provide a concrete justification as to what is in adequate with the product.",
      "Document 3":
        "Software is also a tough problem to solve, at this point I think politics it would even be a tough enough problem. Software I like because outcome having impact. This is the paint brush which I currently hold.",
      Ramblings:
        "One thing I believe is that it is important to enable a distributed mass of people to be successful. If I look at the software that a company creates, they could try to monopolize it for themselves and use it as a moat for any competitors. They could aim to become the sole provider of this service, that might get them a lot of money in the long run but that is not the outcome which I believe it. The outcome which is more important is to provide tools, to provide enablement to other people. You must provide a way for others to succeed in doing something. A good business which offers a service to others, offers others an opportunity for their business to become successful. In addition as opposed to trying to internalize everything yourself, which me more likely than not lead to failure, you take advantage of the wisdom of the crowd. See you for example you provided you created a new way for pizza to be made very effectively, would you rather try to set up a local artist pizza store in hundreds of cities, or sell your system to many existing pizza places, and allow them all to level up their game. If you are more of an enabler then trying to build a MONOPOLY, then you do not need to tackle the problem of localization and you distribute your risk across many businesses. It may be attempting to build your empire. A question to ask also is how am I going to tackle the problem of the right people: finding the right individuals to work with on my start up. A program like next 36 would help me find other individuals that are the right people to work with. But you could also ask the question what are the careers in which I’m going to meet the most new people to expose me to the people I need to meet to make a start up a success. The second question is the right problem: what do I want to solve, the issue is there is an abundance of work on simple problems or common problems that the average individual is exposed to. What there is not enough in a innovation in are the less obvious problems, the problems for which you need to have domain understanding. A problem which may exist for only one kind of business which you may never get the opportunity to work for but you are the right person to taco that problem. The company I worked out this summer fell into a good problem space they were not aiming to help accountants but accountants needed their system, the outcome was that accountants help secure the business towards this massive opportunity for this business. But the founders set out to work on a consumer problem not a bead to be a problem."
    }
  };

  componentDidUpdate(prevProps, prevState, history) {
    if (prevProps.location.pathname !== this.props.location.pathname)
      this.setState({ editorState: this.getContentFromState() });
  }

  componentDidMount() {
    if (this.state.searched === false) {
      this.setState({
        editorState: this.getContentFromState(),
        searched: true
      });
    }
  }

  getContentFromState = () => {
    // find document in state
    let documentTitle = decodeURI(this.props.match.params.documentName);
    let content = this.state.documents[documentTitle];
    if (content) return this.renderForEditor(content);
    else EditorState.createEmpty();
  };

  renderForEditor = content => {
    return EditorState.createWithContent(
      ContentState.createFromBlockArray(convertFromHTML(content))
    );
  };

  onEditorStateChange = editorState => {
    this.setState({ editorState });
    let html = draftToHtml(convertToRaw(editorState.getCurrentContent()));

    // save in DB
    let documentTitle = decodeURI(this.props.match.params.documentName);
    let oldDocuments = this.state.documents;
    oldDocuments[documentTitle] = html;
    this.setState({ documents: oldDocuments });
  };

  render() {
    return (
      <div style={{ flex: 1 }}>
        <Editor
          toolbarClassName="demo-toolbar-absolute"
          wrapperClassName="demo-wrapper"
          editorClassName="demo-editor"
          editorStyle={{ paddingLeft: 20, paddingRight: 20 }}
          // toolbarOnFocus
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
          editorState={this.state.editorState}
          onEditorStateChange={this.onEditorStateChange}
        />
      </div>
    );
  }
}
