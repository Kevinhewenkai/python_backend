'''
class Channel:
    def _init_(self) :
        self.channel_id = 1
        self.name = ""
        self.owners = []
        self.members = []
        self.messages = []
    
    def advance_channel_id(self) :
        self.channel_id += 1
'''

num_users = 0
num_channels = 0
num_messages_created = 0

data = {
    'users': [],
    'channels': [],
}