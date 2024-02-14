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
        {chat.user_ids}
      </div>
      <div className="chat-list-item-detail">
        {chat.created_at}
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
    <div className="chat-list">
      { messages.map((message) =>
        <MessageCard key={message.id} message={message}/>
      )}
    </div>
  )
}

function MessageCard({ message }) {
  const attributes = [
    "user_id",
    "text",
    "created_at"
  ];

  return (
    <div className="chat-card">
      {attributes.map((attr) => (
        <div key={attr} className="chat-card-attr">
          {attr}: {message[attr].toString()}
        </div>
      ))}
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
        <h2>chats</h2>
        <ChatList chats={data.chats} />
      </div>
    )
  }

  return (
    <h2>chat list</h2>
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
      {chatId ? <ChatCardQueryContainer chatId={chatId} /> : <h2>pick a chat</h2>}
    </div>
  );
}

export default ChatPage;