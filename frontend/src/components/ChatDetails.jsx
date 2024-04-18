import { useState } from "react";
import { useMutation, useQueryClient, useQuery } from "react-query";
import { useParams } from "react-router-dom";
import { useApi, useUser } from "../hooks";

function DetailsContainer({chatId, }){
  const user = useUser();
  const [is_owner, isOwner] = useState(false);
  const [owner_id, Owner] = useState("");
  const [checked, checking] = useState(false);
  const queryClient = useQueryClient();
  const { data } = useQuery({
    queryKey: ["chatsUsers", chatId],
    queryFn: () => (
      fetch(`http://127.0.0.1:8000/chats/${chatId}?include=users`)
        .then((response) => response.json())
    ),
  });
  if(data && data.users){
    if(user.id == data.chat.owner.id && !checked){
      checking(true);
      Owner(user.id);
      isOwner(true);
    }else if (!checked){
      checking(true);
      Owner(data.chat.owner.id);
      isOwner(false);
    }

    return (
      <div className="flex flexbox justify-center">
        <div className="min-w-96">
          <ChatNameContainer overallName={data.chat.name} queryClient={queryClient} chatId={chatId} isOwner={is_owner}/>
          <UserListContainer members={data.users} queryClient={queryClient} chatId={chatId} isOwner={is_owner} ownerId={owner_id}/>
        </div>
      </div>
    )
  }
  return (<div>loading...</div>)
}

function ChatNameContainer({overallName, queryClient, chatId, isOwner}){
  const api = useApi();
  const [name, setName] = useState("");
  const mutation = useMutation({
    mutationFn: () => (
      api.put(
        `/chats/${chatId}`,
        {
          name
        }
      ).then((response) => response.json())
    ),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ["chatsUsers"],
      });
      setName("");
    },
  });

  const onSubmit = (e) => {
    e.preventDefault();
    mutation.mutate();
  }
  return(
    <form onSubmit={onSubmit} className="outline-double rounded max-w-md mx-3 my-4 px-2 py-4">
      <h1>{overallName}</h1>
      <div className="flex flexbox w-full">
      <input hidden={!isOwner} type="text" className="text-black px-1" placeholder="chatName" value={name} onChange={(e)=> setName(e.target.value)}></input>
      <div className="flex-1"></div>
      <button hidden={!isOwner} className="bg-orange-700 px-1 rounded hover:bg-orange-500" type="submit">Update</button>
      </div>
    </form>
  )
}

function UserListContainer({members, queryClient, chatId, isOwner, ownerId}){
  const api = useApi();
  const [newMember_id, setMemberID] = useState("");
  const [removeMember_id, removeMemberID] = useState("");

  const addMutation = useMutation({
    mutationFn: () => (
      api.put(
        `/chats/${chatId}/users/${newMember_id}`
      ).then((response) => response.json())
    ),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ["chatsUsers"]
      });
      setMemberID("");
    },
  });

  const add = (e) => {
    e.preventDefault();
    addMutation.mutate();
  }

  const removeMutation = useMutation({
    mutationFn: () => (
      api.del(
        `/chats/${chatId}/users/${removeMember_id}`
      )
    ),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["chatsUsers"]
      });
      removeMemberID("");
    },
  });

  const remove = (e) => {
    e.preventDefault();
    removeMutation.mutate();
  }
  
  const { data } = useQuery({
    queryKey: ["chatDetailsAllUsers"],
    queryFn: () => (
      fetch(`http://127.0.0.1:8000/users`)
        .then((response) => response.json())
    ),
  });

  if(data && data.users){
    //this receives the relative compliment
  var aa = members,
      bb = data.users,
      comparison = (a, b) => a.id === b.id,
      result = bb.filter(b => aa.every(a => !comparison(a, b)));


    return(
      <div className="outline-double rounded max-w-md mx-3 my-4 py-4 px-2">
        <h1>Members</h1>
        <div className="py-1 my-1">
          {
          members.map((user)=>
              <form onSubmit={remove} className="flex flex-box w-full my-1">
                <label className={user.id == ownerId ? "text-green-300": ""}>{user.id == ownerId ? user.username + " - Owner": user.username + " - Member"}</label>
                <div className={"flex-1"}/>
                <button hidden={!isOwner} className="bg-red-700 rounded bold px-1 hover:bg-red-500" onClick={(e)=> removeMemberID(e.target.value)} value={user.id} type="submit">Remove</button>
              </form>
            )
          }
            
        </div>
        <div hidden={!isOwner}>
          <form  onSubmit={add} className="flex flexbox w-full my-2">
            <select onChange={(e)=> setMemberID(e.target.value)} value={newMember_id} className="text-black" id="cars" name="cars">
              <option value=""></option>
              {
                result.map((user) => 
                  <option value={user.id}>{user.username}</option>
                )
              }
            </select>
            <div className="flex-1"></div>
            <button className="bg-green-700 px-1 rounded bold hover:bg-green-500" type="submit">Add</button>
          </form>
        </div>
      </div>
    )
  }
  return(<div>loading...</div>)
  
}

function ChatDetails(){
  const { chatId } = useParams();
  return(
  <div>
    {chatId ? 
    <div className="place-content-center">
      <DetailsContainer chatId={chatId}/>
    </div>
    : 
    <div>Select a chat</div>}
  </div>
  );
}

export default ChatDetails