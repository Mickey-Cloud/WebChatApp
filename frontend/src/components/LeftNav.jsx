import { useState } from "react";
import { NavLink } from "react-router-dom";
import { useQuery } from "react-query";

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

  return (
    <nav className="flex flex-col border-r-2 border-purple-400 h-main">
      <div className="flex flex-col overflow-y-scroll border-b-2 border-purple-400">
        {chats.map((chat) => (
          <Link key={chat.id} chat={chat} />
        ))}
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