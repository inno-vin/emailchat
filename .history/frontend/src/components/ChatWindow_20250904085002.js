import React, { useEffect, useState } from 'react';
import axios from 'axios';

function ChatWindow({ chatId }) {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");

  useEffect(() => {
    if (chatId) {
      axios.get(`http://127.0.0.1:8000/api/messages/?chat=${chatId}`)
        .then(res => setMessages(res.data))
        .catch(err => console.error(err));
    }
  }, [chatId]);

  const sendMessage = () => {
    axios.post("http://127.0.0.1:8000/api/messages/", {
      chat: chatId,
      sender: 2,  // Replace with logged-in user ID
      content: newMessage
    }).then(res => {
      setMessages([...messages, res.data]);
      setNewMessage("");
    });
  };

  return (
    <div>
      <div style={{ height: "300px", overflowY: "scroll", border: "1px solid gray", marginBottom: "10px" }}>
        {messages.map((msg, idx) => (
          <div key={idx}>
            <b>User {msg.sender}:</b> {msg.content}
          </div>
        ))}
      </div>
      <input 
        type="text" 
        value={newMessage} 
        onChange={(e) => setNewMessage(e.target.value)} 
        placeholder="Type a message..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default ChatWindow;
