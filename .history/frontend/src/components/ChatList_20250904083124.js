import React, { useEffect, useState } from "react";
import API from "../services/api";

function ChatList({ onSelectChat }) {
  const [chats, setChats] = useState([]);

  useEffect(() => {
    API.get("chats/")
      .then((res) => setChats(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h2>Chats</h2>
      {chats.map((chat) => (
        <div
          key={chat.id}
          onClick={() => onSelectChat(chat)}
          style={{ cursor: "pointer", borderBottom: "1px solid #ddd", padding: "5px" }}
        >
          Chat #{chat.id}: {chat.user1} & {chat.user2}
        </div>
      ))}
    </div>
  );
}

export default ChatList;
