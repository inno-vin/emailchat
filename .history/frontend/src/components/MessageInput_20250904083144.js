import React, { useState } from "react";
import API from "../services/api";

function MessageInput({ chat, sender }) {
  const [content, setContent] = useState("");

  const sendMessage = () => {
    if (chat && content.trim() !== "") {
      API.post("messages/", {
        chat: chat.id,
        sender: sender,
        content: content,
      })
        .then(() => setContent(""))
        .catch((err) => console.error(err));
    }
  };

  return (
    <div style={{ marginTop: "10px" }}>
      <input
        type="text"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Type a message..."
        style={{ width: "80%", padding: "5px" }}
      />
      <button onClick={sendMessage} style={{ marginLeft: "5px" }}>Send</button>
    </div>
  );
}

export default MessageInput;
