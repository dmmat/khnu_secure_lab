import datetime
import random
import string
import uuid


class Credentials:
    def __init__(self, email, uid):
        self.email = email
        char_set = string.ascii_uppercase + string.digits + string.ascii_letters
        _uuid = uuid.UUID(uid)
        self.key = ''.join(random.sample(char_set * 26, 256))
        self.uid = '-'.join(_uuid.__str__().split('-')[1:5])
        self.created_at = datetime.datetime.fromtimestamp((_uuid.time - 0x01b21dd213814000) * 100 / 1e9)

    def to_dic(self):
        return {
            'email': self.email,
            'key': self.key,
            'uid': self.uid,
            'created_at': self.created_at.isoformat()
        }
