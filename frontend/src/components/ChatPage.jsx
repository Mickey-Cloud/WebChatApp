import { useQuery } from "react-query";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";
import "./ChatPage.css";

function ChatPreview({ chat }) {
    return (
        <Link className="chat-preview" to={`/chats/${chat.id}`}>
            <div className="chat-name">{chat.name}</div>
            <div className="chat-detail">{chat.user_ids}</div>
            <div className="chat-detail">created at: {chat.created_at}</div>
        </Link>
    );
}

function ChatCardWrapper() {
    const { chatId } = useParams();
    if (!chatId) {
        return <ChatCard chat={{}} />
    }

    const navigate = useNavigate();
    const { data, isLoading } = useQuery({
        queryKey: ["chats", chatId],
        queryFn: () => (
            fetch(`http://127.0.0.1:8000/chats/${chatId}/messages`)
                .then((response) => {
                    if (!response.ok) {
                        /*response.status === 404 ?
                            navigate("/error/404") :
                            navigate("/error");*/
                    }
                    return response.json()
                })
        ),
    });

    if (isLoading) {
        return <ChatCard chat={{}} />;
    }

    if (data?.messages) {
        return <ChatCard meta={data.meta} messages={data.messages} />;
    }

    /*return <Navigate to="/error" />;*/
    return <div> Error hello </div>;
}

function ChatCard({ meta, messages }) {
    return (
        <div className="chat-card">
            <h2 className="chat-card-title">Count: {meta.count || "0"}</h2>
            <hr />
            {<div>{"message" || "Messages = 0"}</div>
            
            }
        </div>
    )
}

function MessageCard({ message }){
    return(
        <div>
            {["user_id", "text", "created_at"].map((attr) => (
                <div key={attr} className="chat-card-row">
                    <div className="chat-detail-category">{attr}</div>
                    <div className="chat-detail-value">
                        {(chat || {})[attr]?.toString() || attr}
                    </div>
                </div>
            ))}
        </div>
    )
}

function EmptyChatList() {
    return <ChatList chats={[0, 1, 2, 3, 4].map(() => ({
        name: "loading...",
        user_ids: "Text of the message",
        created_at: "Date - time",
    }))} />
}

function ChatList({ chats }) {
    return (
        <div className="chat-list">
            {chats.map((chat) => (
                <ChatPreview key={chat.id} chat={chat} />
            ))}
        </div>
    );
}

function ChatPage() {
    const navigate = useNavigate();
    const { data, isLoading, error } = useQuery({
        queryKey: ["chats"],
        queryFn: () => (
            fetch("http://127.0.0.1:8000/chats")
                .then((response) => {
                    if (!response.ok) {
                        response.status === 404 ?
                            navigate("/error/404") :
                            navigate("/error");
                    }
                    return response.json()
                })
        ),
    });

   /* if (error) {
        return <Navigate to="/error" />
    }*/

    return (
        <>
            <h1>chats</h1>
            <div className="chats-page">
                {!isLoading && data?.chats ?
                    <ChatList chats={data.chats} /> :
                    <EmptyChatList />
                }
                <ChatCardWrapper />
            </div>
        </>
    );
}

export default ChatPage;