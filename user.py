import collections.abc # For Hashable check
import pickle


class User:

    # ID = 0 for the bot user
    BOT_AS_USER_ID = 0

    __userlist = set()

    @classmethod
    def get_userlist(cls):
        return cls.__userlist

    @classmethod
    def save_userlist(cls):
        with open ("bot_chat_history.pkl", 'wb') as f:
            pickle.dump(cls.__userlist, f)

    @classmethod
    def load_userlist(cls):
        try:
            with open("bot_chat_history.pkl", 'rb') as f:
                cls.__userlist = pickle.load(f)
        except FileNotFoundError:
            cls.__userlist = set()
        except EOFError:
            cls.__userlist = set()
        except Exception as e:
            print(f"An error occurred while loading user list: {e}")
            cls.__userlist = set()

    def __init__(self, id:str, tag:str, model:str = "deepseek-chat"):
        self._id = id
        self._tag = tag
        self._messages = []
        self._model = model
        User.__userlist.add(self)
    
    def set_model(self, model:str):
        self._model = model

    def get_model(self):
        return self._model if self._model else "deepseek-chat"
        
    def __str__(self):
        return f"User {self._id}, with tag {self._tag} and {len(self._messages)} messages."
    
    def get_id(self):
        return self._id
    
    def get_tag(self):
        return self._tag
    
    def get_messages(self):
        return self._messages

    def add_message(self, message):
        self._messages.append(message)

    def delete_conversation(self):
        self._messages = []

    def __eq__(self, user):
        return self.get_id() == user.get_id()

    def __hash__(self):
        return hash(self.get_id())

    def get_conversation(self):
        conversation = ""
        for msg in self._messages:
            if msg.is_from_bot():
                conversation += f"YOU: {msg.get_text()}\n"
            else:
                conversation += f"USER: {msg.get_text()}\n"
        return conversation
       
    def get_conversation_for_bot(self):
        list_of_messages = []
        for msg in self._messages:
            role = "assistant" if msg.is_from_bot() else "user"
            content = msg.get_text()
            
            # Merge consecutive messages with the same role
            if list_of_messages and list_of_messages[-1]["role"] == role:
                if list_of_messages[-1]["content"] != content: 
                    list_of_messages[-1]["content"] += "\n new mesage: \n" + content
            else:
                list_of_messages.append({"role": role, "content": content})
        
        return list_of_messages

    @classmethod
    def get_user_by_id(cls,user_id, tag):
        #finds user if there is, or creates a new one
        for user in User.get_userlist():
            if user.get_id() == user_id:
                return user
        return User(user_id, tag)



class Message:
    
    def __init__(self, id:int, text:str, is_from_bot:bool, chat:int, date:str):
        self._date = date
        self._id = id
        self._text = text
        self._is_from_bot = is_from_bot
        self._chat = chat
        
    
    def get_text(self):
        return self._text
    
    def is_from_bot(self):
        return self._is_from_bot
    
    def get_chat(self):
        return self._chat
    
    def get_date(self):
        return self._date
