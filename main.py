from messanger import Messanger
from config import token

messanger = Messanger(
    token=token
)

while True:
    messanger.get_user_chats()

    if messanger.now_chat:
        messanger.get_messages()
    else:
        messanger.get_chats()