import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import { useState } from "react";

function ChatListItem({ chat, onClick }) {
  
  return (
    <Link key={chat.id} to={`/chats/${chat.id}`} className="chat-list-item" onClick={onClick}>
      <div className="chat-list-item-name">
        {chat.name}
      </div>
      <div className="chat-list-item-detail">
        Owner: {chat.owner.username}
      </div>
      <div className="chat-list-item-detail">
        Date: {new Date(chat.created_at).toLocaleDateString()}
      </div>
    </Link>
  )
}

function ChatList({ chats, setMessageName}) {
  return (
    <div className="chat-list">
      {chats.map((chat) => (
        <ChatListItem key={chat.id} chat={chat}  onClick={() => setMessageName(chat.name)} />
      ))}
    </div>
  )
}

function MessageList({ messages }){
  return(
    <div className="message-list-container">
      <div className="message-list">
        { messages.map((message) =>
          <MessageCard key={message.id} message={message}/>
        )}
      </div>
    </div>
  )
}

function MessageCard({ message }) {
  const date = new Date(message.created_at)

  return (
    <div className="message-box">
      <div>
        <span className="message-user" >{message.user_id}</span>
        <span className="message-date-time">{date.toDateString()  + "    -   " + date.toLocaleTimeString()} </span>
      </div>
      <div className="message-container">
        <div className="message">
          {message.text}
        </div>
      </div>
    </div>
  )
}

function ChatCardContainer({ messages, messageName }) {
  return (
    <div className="chat-card-container">
      <h2>{messageName}</h2>
      <MessageList messages={messages} />
    </div>
  );
}

function ChatListContainer( {setMessageName}) {
  const { data } = useQuery({
    queryKey: ["chats"],
    queryFn: () => (
      fetch("http://127.0.0.1:8000/chats")
        .then((response) => response.json())
    ),
  });

  if (data?.chats) {
    return (
      <div className="chat-list-container">
        <h2>Chats</h2>
        <ChatList chats={data.chats} setMessageName={setMessageName} />
      </div>
    )
  }

  return (
    <h2>Chat List</h2>
  );
}

function ChatCardQueryContainer({ chatId, messageName }) {
  const { data } = useQuery({
    queryKey: ["chats", chatId],
    queryFn: () => (
      fetch(`http://127.0.0.1:8000/chats/${chatId}/messages`)
        .then((response) => response.json())
    ),
  });

  if (data && data.messages) {
    return <ChatCardContainer messages={data.messages} messageName={messageName} />
  }

  return <h2>loading...</h2>
}

function ChatPage() {
  const { chatId } = useParams();
  const [MessageName, setMessageName] = useState(
    "none",
  );
  return (
    <div className="chats-page">
      <ChatListContainer setMessageName={setMessageName}/>
      {chatId ? <ChatCardQueryContainer chatId={chatId} messageName={MessageName} /> : <h2>Select a chat</h2>}
    </div>
  );
}

export default ChatPage;