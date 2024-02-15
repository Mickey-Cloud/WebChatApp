import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import "./ChatPage.css";

function ChatListItem({ chat }) {
  return (
    <Link key={chat.id} to={`/chats/${chat.id}`} className="chat-list-item">
      <div className="chat-list-item-name">
        {chat.name}
      </div>
      <div className="chat-list-item-detail">
        Participants: <br/>{chat.user_ids.join(", ")}
      </div>
      <div className="chat-list-item-detail">
        Date: {new Date(chat.created_at).toLocaleDateString()}
      </div>
    </Link>
  )
}

function ChatList({ chats }) {
  return (
    <div className="chat-list">
      {chats.map((chat) => (
        <ChatListItem key={chat.id} chat={chat} />
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

function ChatCardContainer({ messages }) {
  return (
    <div className="chat-card-container">
      <h2>Messages</h2>
      <MessageList messages={messages} />
    </div>
  );
}

function ChatListContainer() {
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
        <ChatList chats={data.chats} />
      </div>
    )
  }

  return (
    <h2>Chat List</h2>
  );
}

function ChatCardQueryContainer({ chatId }) {
  const { data } = useQuery({
    queryKey: ["chats", chatId],
    queryFn: () => (
      fetch(`http://127.0.0.1:8000/chats/${chatId}/messages`)
        .then((response) => response.json())
    ),
  });

  if (data && data.messages) {
    return <ChatCardContainer messages={data.messages} />
  }

  return <h2>loading...</h2>
}

function ChatPage() {
  const { chatId } = useParams();
  return (
    <div className="chats-page">
      <ChatListContainer />
      {chatId ? <ChatCardQueryContainer chatId={chatId} /> : <h2>Select a chat</h2>}
    </div>
  );
}

export default ChatPage;