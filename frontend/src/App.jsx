import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, NavLink, Navigate, Routes, Route } from 'react-router-dom';
import { AuthProvider, useAuth } from "./context/auth";
import { UserProvider, useUser } from './context/user';

import Registration from "./components/Registration";
import Profile from "./components/Profile";
import ChatPage from './components/ChatPage';
import TopNav from "./components/TopNav";
import Login from "./components/login";

const queryClient = new QueryClient();

function NotFound() {
  return <h1>404: not found</h1>;
}

function Home() {
  const { isLoggedIn, logout } = useAuth();

  return (
    <div className="max-w-4/5 mx-auto text-center px-4 py-8">
      <div className="py-2">
        logged in: {isLoggedIn.toString()}
      </div>
    </div>
  );
}

function Header() {
  return (
    <header>
      <TopNav />
    </header>
  );
}

function AuthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/chats" element={<ChatPage />}>
        <Route path="/chats/:chatId" element={<ChatPage />} />
      </Route>
      <Route path="/profile" element={<Profile />}/>
      <Route path="/error/404" element={<NotFound />} />
      <Route path="*" element={<Navigate to="/error/404" />} />
    </Routes>
  );
}

function UnauthenticatedRoutes(){
  return(
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/registration" element={<Registration />} />
      <Route path="*" element={<Navigate to="/login" />} />
      {/*<Route path="/error" element={<div>Error</div>}/>*/}
    </Routes>
  )
}

function Main(){
  const { isLoggedIn } = useAuth();

  return (
    <main className="max-h-main">
      {isLoggedIn ?
        <AuthenticatedRoutes/> :
        <UnauthenticatedRoutes/>
      }
    </main>
  );
}




function App() {
  const className = [
    "h-screen max-h-screen",
    "max-w-2xl mx-auto",
    "bg-gray-700 text-white",
    "flex flex-col",
  ].join(" ");

  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
      <BrowserRouter>
          <UserProvider>
            <div className={className}>
              <Header/>
              <Main/>
            </div>
          </UserProvider>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App
