import random
from datetime import datetime, timedelta, timezone


class RecoveryCode():     
    def __init__(self, minutes_of_code_lifetime: int, code: str = None):
        self.code = "".join(str(random.randint(0, 9)) for _ in range(5)) if code is None else code
        self.expired_datetime = datetime.now(timezone.utc)  + timedelta(minutes= minutes_of_code_lifetime)

    def is_valid(self):
        return self.expired_datetime > datetime.now(timezone.utc)
    