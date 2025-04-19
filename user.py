import collections.abc # For Hashable check

class User:

    __userlist = set()

    def get_userlist():
        return User.__userlist

    def __init__(self, id:str, tag:str):
        self._id = id
        self._tag = tag
        self._messages = []
        User.__userlist.add(self)
        
    def __str__(self):
        return f"User {self._id} with tag {self._tag}"
    
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

class message:
    
      def __init__(self, id:int, text:str, sender:User, chat:User, date:str):
        self._date = date
        self._id = id
        self._text = text
        self._sender = sender
        self._chat = chat