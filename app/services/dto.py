from typing import NamedTuple


class UserDTO(NamedTuple):
    id: int
    tg_id: int
    username: str
