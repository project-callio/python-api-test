from dataclasses import dataclass, field

from convclasses import mod


@dataclass
class RegisterReq:
    username: str
    password_hash: str
    email: str
    full_name: str = field(default=None)
    comment: str = field(default=None)
