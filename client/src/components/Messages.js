import React, { useCallback } from "react";

const Messages = ({  channelMessages }) => {
  const setRef = useCallback((node) => {
    if (node) {
      node.scrollIntoView({ behavior: "smooth" });
    }
  }, []);

  const chatMessages = channelMessages.map((chat, index) => {
    return (
      <div key={index} ref={setRef} className="bubble">
        <p style={{ fontWeight: "bold", marginRight: "5px" }}>{chat.user}</p>
        <p>{chat.text}</p>
      </div>
    );
  });

  return (
    <div className="col-md-6 pl-0">
      <div className="card card-bordered">
        <div className="card-header">
          <h4 className="card-title">
            <strong>Chat</strong>
          </h4>
        </div>

        <div
          className="ps-container ps-theme-default ps-active-y"
          id="chat-content"
          style={{
            overflow: "scroll !important",
            height: "400px !important",
          }}
        >
          <div>
            <div>
              <div>{chatMessages}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Messages;
