
function NewChat(){
  return(
    <form className="border max-w-md m-2 p-2 rounded">
      <h1>Chat Name</h1>
      <input className="text-red-300 my-3" type="text" placeholder="New Chat Name"></input>
      <div></div>
      <button className="p-1 rounded bg-red-900 text-pint-200 border-fuchsia-800 border hover:bg-red-500" type="submit">Create</button>
    </form>
  );
}

export default NewChat