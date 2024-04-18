import { useState } from "react";
import { NavLink } from "react-router-dom";
import { useQuery } from "react-query";
import { useRef } from "react";

const emptyChat = (id) => ({
  id,
  name: "loading...",
  empty: true,
});

function Link({ chat }) {
  const url = chat.empty ? "#" : `/chats/${chat.id}`;
  const className = ({ isActive }) => [
    "p-2",
    "hover:bg-slate-800 hover:text-grn",
    "flex flex-row justify-between",
    isActive ?
      "bg-slate-800 text-grn font-bold" :
      ""
  ].join(" ");

  const chatName = ({ isActive }) => (
    (isActive ? "\u00bb " : "") + chat.name
  );

  return (
    <NavLink to={url} className={className}>
      {chatName}
    </NavLink>
  );
}

function LeftNav() {
  const [search, setSearch] = useState("");

  const { data } = useQuery({
    queryKey: ["chats"],
    queryFn: () => (
      fetch("http://127.0.0.1:8000/chats")
        .then((response) => response.json())
    ),
  });

  const regex = new RegExp(search.split("").join(".*"));

  const chats = ( data?.chats || [1, 2, 3].map(emptyChat)
  ).filter((chat) => (
    search === "" || regex.test(chat.name)
  ));

  const outerRef = useRef(0);
  const innerRef = useRef(0);
  const outerHeight = outerRef.current.clientHeight;
  const innerHeight = innerRef.current.clientHeight;

  const leftNavScrollClass = [
    "flex flex-col",
    "border-b-2",
    "border-purple-400",
    (innerHeight+60 >= outerHeight)?
    "overflow-y-scroll":
    "overflow-y-hidden"
  ].join(" ");

  return (
    <nav ref={outerRef} className="flex flex-col border-r-2 border-purple-400 h-main">
      <div ref={innerRef} className={leftNavScrollClass} >
        {chats.map((chat) => (
          <Link key={chat.id} chat={chat} />
        ))}
      </div>
      <div className="my-5 w-full flex">
        <NavLink className="p-1 w-screen rounded text-center bg-red-900 text-pint-200 border-fuchsia-800 border m-2 hover:bg-red-500" to={"/chats/new"}>New Chat</NavLink>
      </div>
      <div className="p-2">
        <input
          className="w-36 px-4 py-2 bg-gray-700 border border-gray-500"
          type="text"
          placeholder="search"
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>
    </nav>
  );
}

export default LeftNav;