from prettytable import PrettyTable
import vk_api
import sys
import os


def transfer_message(text: str):
    if len(text) > 15:
        new_text = ''
        words_count = 0
        for word in text.split():
            if words_count > 3:
                words_count = 0
                new_text += '\n'
            new_text += word + ' '
            words_count += 1
        text = new_text
    return text


class Messanger:
    def __init__(self, token: str):
        self.tables_manager = PrettyTable()
        self.tables_manager.field_names = [
            'pk', 'username', 'message'
        ]

        self.session = vk_api.VkApi(
            token=token
        )
        self.api = self.session.get_api()
        self.chats = {}
        self.in_chat = False
        self.now_chat = None
        self.get_chats()

        user_data = self.session.method(
            'users.get'
        )[0]
        self.now_user_name = user_data['first_name']
        self.now_user_id = user_data['id']

    def clear_console(self):
        os.system(['clear', 'cls'][os.name == sys.platform])

    def get_messages(self):
        messages = self.session.method('messages.getHistory', {
            'user_id': self.now_chat,
            'count': 10
        })
        user_info = self.session.method('users.get', {
            'user_ids': [
                self.now_chat
            ]
        })[0]
        self.clear_console()

        print(f'{user_info["first_name"]} {user_info["last_name"]}')
        for message in messages['items'][::-1]:
            if message['text']:
                if message['from_id'] == self.now_user_id:
                    print('\n(' + self.now_user_name + ') - ' + message['text'])
                else:
                    print('\n(' + user_info["first_name"] + ') - ' + message['text'])
        print('\n>>> ', end='')

    def send_message(self, text):
        if text:
            self.session.method('messages.send', {
                'user_id': self.now_chat,
                'random_id': 0,
                'message': text
            })

    def get_chats(self):
        chats = self.session.method(
            'messages.getConversations', {
                'count': 10
            })

        if not self.in_chat:
            pk = 0
            for chat in chats['items']:
                if '-' not in str(chat['conversation']['peer']['id']):
                    user_info = self.session.method('users.get', {
                        'user_ids': [
                            chat['conversation']['peer']['id']
                        ]
                    })[0]
                    if user_info["first_name"] != 'DELETED':
                        self.chats[pk] = chat['conversation']['peer']['id']
                        self.tables_manager.add_row(
                            [
                                f'\n{pk}',
                                f'\n{user_info["first_name"]} '
                                f'\n{user_info["last_name"]}',
                                '\n{}'.format(
                                    transfer_message(
                                        chat['last_message']['text']
                                    )
                                )
                            ]
                        )
                        pk += 1

            self.clear_console()
            print(self.tables_manager)
            self.tables_manager.clear_rows()
        else:
            self.get_messages()

    def get_user_chats(self):
        text = input()

        if text.isdigit():
            chat_id = int(text)
            if not self.in_chat:
                for i in self.chats:
                    if chat_id == i:
                        self.now_chat = self.chats[i]
                        self.in_chat = True
                self.tables_manager.clear_rows()

        elif text == 'back':
            self.tables_manager.clear_rows()
            self.in_chat = False
            self.now_chat = None

        elif text == 'update':
            if self.now_chat:
                self.get_messages()
            else:
                self.get_chats()
        else:
            self.send_message(text)
