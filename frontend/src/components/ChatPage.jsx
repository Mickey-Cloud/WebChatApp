import { useMutation, useQueryClient, useQuery } from "react-query";
import { useState } from "react";
import { NavLink, useParams } from "react-router-dom";
import { useUser } from "../context/user";
import { useApi } from "../hooks";
import { useNavigate } from "react-router-dom";
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
  const [dialogOpen, closeDialogHandler] = useState(false);
  const [text, changeMessage] = useState(`${message.text}`);
  const user = useUser();
  const queryClient = useQueryClient();
  const username = user.username;
  const api = useApi();

  const deleteMutation = useMutation({
    mutationFn: () => (
      api.del(
        `/chats/${message.chat_id}/messages/${message.id}`,
      ).then(() => 1)
    ),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ["chats"]
      });
    },
  });
  const onDelete = (e) => {
    e.preventDefault();
    deleteMutation.mutate();
  }

  return (
    <>
    {message.user.username == username ?
      <div className="px-1 py-1 rounded">
        <div className="flex flex-box">
          <div className="flex-1"/>
          <div className="opacity-0 hover:opacity-100" >
            <span className="text-xs mx-1">{date.toDateString()  + "    -   " + date.toLocaleTimeString()} </span>
            <button onClick={()=> closeDialogHandler(true)} className="text-xs px-1 rounded bg-blue-500 mx-1">Edit</button>
            <button onClick={onDelete} className="text-xs px-1 rounded bg-red-500 mx-1 ">Delete</button>
          </div>
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
    {
      dialogOpen && <DialogBox onCancel={closeDialogHandler} text={text} changeMessage={changeMessage} message={message} api={api} queryClient={queryClient}/>
    }
    </>
  )
}

function DialogBox({onCancel, text, changeMessage, message, api, queryClient}){
  const navigate = useNavigate();
  const editMutation = useMutation({
    mutationFn: () => (
      api.put(
        `/chats/${message.chat_id}/messages/${message.id}`,
        {
          text
        }
      ).then((response) => response.json())
    ),
    onSuccess: (data) => {
      console.log("here");
      queryClient.invalidateQueries({
        queryKey: ["chats"]
      });
      navigate(`/chats/${message.chat_id}`);
    },
  });
  const onEdit = (e) => {
    e.preventDefault();
    onCancel(false);
    editMutation.mutate();
  }
  return(
  <form onSubmit={onEdit} className="rounded min-w-80 fixed px-4 py-2 bg-gray-900 top-1/2 left-1/2 border">
    <h3>New Message</h3>
    <input className="w-full text-black px-1" type="text" value={text} onChange={(e)=> changeMessage(e.target.value)}></input>
    <div className="flex-1"></div>
    <div className="flex flexbox">
      <div className="flex-1"/>
      <button type="submit" className="bg-green-500 px-2 mt-2 rounded" >Save</button>
      <button type="button" className="bg-red-500 px-2 mx-4 mt-2 rounded" onClick={()=> onCancel(false)}>Cancel</button>
    </div>
    
  </form>
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
  const api = useApi();
  const queryKey = ["chats", chatId]
  const { data } = useQuery({
    queryKey,
    queryFn: () => (
      api.get(`/chats/${chatId}/messages`)
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