import { NavLink } from "react-router-dom";

function Home() {
  const url = "/login"

  return (
    <div className="max-w-4/5 mx-auto text-center px-4 py-8">
      <div className="py-2">
        <h1>Pony Express</h1>
        <p className="p-2">
          A chat application, where users that are logged in can communicate through messages.
        </p>
        <br/>
        <NavLink to={url} className="p-2 hover:bg-slate-800 hover:text-rose-400 border rounded">Get Started</NavLink>
      </div>
    </div>
  );
}

export default Home;