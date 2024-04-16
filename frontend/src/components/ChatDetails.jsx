
function ChatNameContainer(){
  return(
    <form className="border max-w-sm mx-3 my-2 p-2">
      <h1>Chat Name</h1>
      <div className="flex flexbox w-full">
      <input type="text" placeholder="chatName"></input>
      <button type="submit">Update</button>
      </div>
    </form>
  )
}

function UserListContainer(){
  return(
    <form className="border mx-3 my-2 p-2">
      <h1>Users</h1>
      <div>
        <div className="flex flex-box w-full">
          <label>userName</label>
          <div className="flex-1"/>
          <button>Remove</button>
        </div>
      </div>
    </form>
  )
}

function ChatDetails(){
  return(
    <div className="max-w-md">
      <ChatNameContainer/>
      <UserListContainer/>

    </div>
  );
}

export default ChatDetails