import datetime
import time
from typing import NamedTuple


class UserDTO(NamedTuple):
    id: int
    tg_id: int
    username: str
    first_name: str


class QuotesTimeDTO(NamedTuple):
    set_send_time: time
    last_send_time: datetime.datetime
