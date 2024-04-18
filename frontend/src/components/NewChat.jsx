import { useState } from "react";
import { useMutation, useQueryClient} from "react-query";
import { useNavigate } from "react-router-dom";
import { useApi } from "../hooks";

function NewChat(){
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const api = useApi();
  const [name, setName] = useState("");
  
  const mutation = useMutation({
    mutationFn: () => (
      api.post(
        `/chats`,
        {
          name
        }
      ).then((response) => response.json())
    ),
    onSuccess: (data) => {
      navigate(`/chats/${data.chat.id}/details`);
      setName("");
    },
  });

  const onSubmit = (e) => {
    e.preventDefault();
    mutation.mutate();
  }
  
  
  return(
    <div className="flex justify-center">
      <form onSubmit={onSubmit} className="border max-w-md m-2 p-2 rounded">
        <h1 className="text-center">Chat Name</h1>
        <input className="text-black w-full my-3" type="text" placeholder="New Chat Name" onChange={(e) => setName(e.target.value)}></input>
        <div></div>
        <button className="p-1 rounded w-full bg-red-900 text-pint-200 border-fuchsia-800 border hover:bg-red-500" type="submit">Create</button>
      </form>
    </div>
    
  );
}

export default NewChat