import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, NavLink, Navigate, Routes, Route } from 'react-router-dom';
import { AuthProvider, useAuth } from "./context/auth";
import { UserProvider } from './context/user';

import Home from "./components/Home"
import Registration from "./components/Registration";
import Profile from "./components/Profile";
import ChatPage from './components/ChatPage';
import TopNav from "./components/TopNav";
import Login from "./components/login";

const queryClient = new QueryClient();

function NotFound() {
  return <h1>404: not found</h1>;
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
      <Route path="/" element={<Navigate to="/chats" />} />
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
    "max-w-5xxl mx-auto",
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
