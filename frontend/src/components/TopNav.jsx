import { NavLink } from "react-router-dom";
import { useAuth } from "../context/auth";
import { useUser } from "../context/user";

function NavItem({ to, name, right }) {
  const className = [
    "border-fuchsia-800",
    "py-2 px-4",
    "hover:bg-slate-700",
    right ? "border-l-2" : "border-r-2"
  ].join(" ")

  const getClassName = ({ isActive }) => (
    isActive ? className + " bg-slate950" : className
  );

  return (
    <NavLink to={to} className={getClassName}>
      {name}
    </NavLink>
  );
}

function AuthenticatedNavItems() {
  const user = useUser();

  return (
    <>
      <NavItem to="/" name="Pony Express" />
      <NavItem to="/chats" name="Chats" />
      <div className="flex-1" />
      <NavItem to="/profile" name={user?.username} right />
    </>
  );
}

function UnauthenticatedNavItems() {
  return (
    <>
      <NavItem to="/" name="Pony Express" />
      <div className="flex-1" />
      <NavItem to="/login" name="Login" right />
      <NavItem to="/registration" name="Register" right/>
    </>
  );
}


function TopNav() {
  const { isLoggedIn } = useAuth();

  return (
    <nav className="flex flex-row border-b-4 border-fuchsia-800">
      {isLoggedIn ?
        <AuthenticatedNavItems /> :
        <UnauthenticatedNavItems />
      }
    </nav>
  );
}

export default TopNav;