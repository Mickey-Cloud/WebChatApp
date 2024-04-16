import { useQuery } from "react-query";
import { Link, NavLink, useParams } from "react-router-dom";
import { useEffect, useRef } from "react";
import { useUser } from "../context/user";
import ScrollContainer from "./ScrollContainer"
import LeftNav from "./LeftNav";
import NewMessage from "./NewMessage";

function MessageList({ messages }){
  return(
    <div className=" px-2 py-3 rounded-md">
      <div className="maxHeight-chat">
        { messages.map((message) =>
          <MessageCard key={message.id} message={message}/>
        )}
      </div>
    </div>
  )
}

function MessageCard({ message }) {
  const date = new Date(message.created_at)
  const user = useUser();
  const username = user.username;

  return (
    <>
    {message.user.username == username ?
      <div className="px-1 py-1 rounded">
        <div className="flex flex-box">
          <div className="flex-1"/>
          <span className="text-xs text-transparent  hover:text-white">{date.toDateString()  + "    -   " + date.toLocaleTimeString()} </span>
        </div>
        <div className="flex flex-box">
          <div className="flex-1"/>
          <div className="border border-pink-800 rounded-xl px-1 max-w-[80%] py-2 w-fit bg-fuchsia-800">
            {message.text}
          </div>
        </div>
      </div>
        :
      <div className="px-1 py-1 rounded">
        <div className="flex flex-box w-full">
          <span className="font-bold text-xs" >{message.user.username}</span>
          <div className="flex-1"/>
          <span className="text-xs text-transparent hover:text-white">{date.toDateString()  + "    -   " + date.toLocaleTimeString()} </span>
        </div>
        <div className="flex flex-box">
          <div className="border border-fuchsia-800 rounded-xl max-w-[80%] px-1 py-2 w-fit bg-pink-700">
            {message.text}
          </div>
        </div>
      </div>
    }
    </>
  )
}

function ChatCardContainer({ messages, chatId }) {
  const url = `/chats/${chatId}/details`
  
  return (
    <div>
      <div className="flex flex-box w-full">
      <div className="flex-1"/>
      <NavLink to={url} className="rounded bg-red-900 text-pink-100 px-2 py-1">Settings</NavLink>
      </div>
      <ScrollContainer>
        <MessageList messages={messages} />
      </ScrollContainer>
    </div>
    
  );
}

function ChatCardQueryContainer({ chatId,  }) {
  const { data } = useQuery({
    queryKey: ["chats", chatId],
    queryFn: () => (
      fetch(`http://127.0.0.1:8000/chats/${chatId}/messages`)
        .then((response) => response.json())
    ),
  });

  if (data && data.messages) {
    return <ChatCardContainer messages={data.messages} chatId={chatId} />
  }

  return <h2>loading...</h2>
}

function ChatPage() {
  const { chatId } = useParams();
  return (
    <div className="flex flex-row h-main">
      <div className="w-40">
        <LeftNav/>
      </div>
      <div>
        {chatId ? 
        <div className="">
          <ChatCardQueryContainer chatId={chatId}  /> 
          <NewMessage chatId={chatId}/>
        </div>
        : 
        <h2>Select a chat</h2>}
      </div>
    </div>
  );
}

export default ChatPage;