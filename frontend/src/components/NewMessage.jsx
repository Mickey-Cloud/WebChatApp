import { useState } from "react";
import { useMutation, useQueryClient } from "react-query";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useAuth, useApi } from "../hooks";
import Button from "./Button";

function Input (props){
  return (
    <div className="flex flex-box py-2 max-h-20 border border-fuchsia-500 rounded-xl w-[90%]">
      <label className="text-s text-gray-400 px-2" htmlFor={props.name}>
        {props.name}
      </label>
      <textarea
        {...props}
        className="w-full h-auto max-h-12 rounded bg-transparent text-wrap mx-2 px-2 min-w-36 "
      />
      <button type="submit" className="border-fuchsia-500 px-2 py-2 bg-purple-950 rounded-xl">Send</button>
    </div>
  );
}

function NewChatForm(){
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const{ token } = useAuth();
  const api = useApi();
  const { chatId } = useParams();

  const [text, setMessage] = useState("");

  const mutation = useMutation({
    mutationFn: () => (
      api.post(
        `/chats/${chatId}/messages`,
        {
          text
        }
      ).then((response) => response.json())
    ),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ["chats"]
      });
      navigate(`/chats/${chatId}`);
      setMessage("");
    },
  });

  const onSubmit = (e) => {
    e.preventDefault();
    mutation.mutate();
  }

  return (
    <form onSubmit={onSubmit}>
      <div className="flex flex-left">
        <Input
          name=""
          type="text"
          value={text}
          onChange={(e)=> setMessage(e.target.value)}
        />
        
      </div>
    </form>
  )

}

function NewMessage(chatId){
  return (
    <div>
      <NewChatForm chatId={chatId} />
    </div>
  );
}

export default NewMessage