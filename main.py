import threading

from messanger import Messanger
from config import token

messanger = Messanger(
    token=token
)

while True:
    get_users_chat_thread = threading.Thread(target=messanger.get_user_chats)
    get_users_chat_thread.start()

    if messanger.now_chat:
        messanger.get_messages()
    else:
        messanger.get_chats()
