import datetime
import uuid

import settings


class Trials:
    def __init__(self, uid):
        _uuid = uuid.UUID(uid)
        self.uid = '-'.join(_uuid.__str__().split('-')[1:5])
        self.created_at = datetime.datetime.fromtimestamp((_uuid.time - 0x01b21dd213814000) * 100 / 1e9)
        self.day_limit = settings.TRIAL_DAY_LIMIT
        self.ended_at = self.created_at + datetime.timedelta(days=self.day_limit)

    def to_dic(self):
        return {
            'uid': self.uid,
            'created_at': self.created_at.isoformat(),
            'ended_at':  self.ended_at.isoformat()
        }
