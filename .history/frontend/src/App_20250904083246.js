import React, { useState } from "react";
import ChatList from "./components/ChatList";
import ChatWindow from "./components/ChatWindow";
import MessageInput from "./components/MessageInput";

function App() {
  const [selectedChat, setSelectedChat] = useState(null);
  const sender = 1; // temporary hardcoded user ID

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <div style={{ width: "30%", borderRight: "1px solid gray", padding: "10px" }}>
        <ChatList onSelectChat={setSelectedChat} />
      </div>
      <div style={{ width: "70%", padding: "10px" }}>
        <ChatWindow chat={selectedChat} />
        {selectedChat && <MessageInput chat={selectedChat} sender={sender} />}
      </div>
    </div>
  );
}

export default App;
