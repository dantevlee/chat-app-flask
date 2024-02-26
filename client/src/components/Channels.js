import React from "react";

const Channels = ({ channels, toggleChannel, selectedChannel }) => {
  const channelList = channels.map((c) => (
    <p
      key={c.id}
      className={selectedChannel === c.channel ? "active-channel" : ""}
      onClick={() => {
        toggleChannel(c.channel);
      }}
      style={{
        cursor: "pointer",
      }}
    >
      #{c.channel}
    </p>
  ));

  return (
    <React.Fragment>
      <div className="col-md-3 pr-0">
        <div className="card card-bordered">
          <div className="card-header">
            <h4 className="card-title">
              <strong>Channels</strong>
            </h4>
          </div>

          <div
            className="ps-container ps-theme-default ps-active-y"
            id="chat-content"
            style={{
              overflow: "scroll !important",
              width: "300px", 
              height: "1000px", 
            }}
          >
            <div>
              <div className="channels">{channelList}</div>
            </div>
          </div>
        </div>
      </div>
    </React.Fragment>
  );
};

export default Channels;
