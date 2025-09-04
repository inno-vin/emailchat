import React, { useEffect, useState } from "react";
import API from "../services/api";

function ChatWindow({ chat }) {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    if (chat) {
      API.get("messages/")
        .then((res) => {
          const filtered = res.data.filter((msg) => msg.chat === chat.id);
          setMessages(filtered);
        })
        .catch((err) => console.error(err));
    }
  }, [chat]);

  if (!chat) return <div>Select a chat to start messaging</div>;

  return (
    <div>
      <h3>Chat #{chat.id}</h3>
      <div style={{ minHeight: "200px", border: "1px solid #ddd", padding: "10px" }}>
        {messages.map((msg) => (
          <div key={msg.id}>
            <strong>User {msg.sender}:</strong> {msg.content}
          </div>
        ))}
      </div>
    </div>
  );
}

export default ChatWindow;
