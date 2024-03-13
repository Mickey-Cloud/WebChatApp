from sqlmodel import Session

from backend import database as db
from backend.schema import (
    UserInDB,
    UserRegistration,
    UserUpdate,
    Chat,
    ChatInDB,
    ChatUpdate,
    ChatCollection,
    MessageInDB,
    Message,
    
)

def chatInDB_to_chat(chat: ChatInDB):
  return Chat(
            id=chat.id,
            name=chat.name,
            owner=chat.owner,
            created_at=chat.created_at
        )

def chatsInDB_to_chats(session: Session) -> list[Chat]:
    chats = db.get_chats(session)
    newChatList = []
    for chat in chats:
        newChatList.append(chatInDB_to_chat(chat))
    return newChatList

def messageInDB_to_Message(message = MessageInDB) -> Message:
  return Message(
            id=message.id,
            text=message.text,
            chat_id=message.chat_id,
            user=message.user,
            created_at=message.created_at
        )
  
def from_MessagesInDB_to_Messages(messageList = list[MessageInDB]) -> list[Message]:
    newMessageList = []
    for message in messageList:
        newMessageList.append(messageInDB_to_Message(message))
    return newMessageList