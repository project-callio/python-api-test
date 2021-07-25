from dataclasses import dataclass, field
from typing import NewType

from apitist.random import Username, Email, str_type
from convclasses import mod


Password = str_type("Password")
FullName = str_type("FullName")
Comment = str_type("Comment")


@dataclass
class RegisterReq:
    username: Username
    password_hash: Password
    email: Email
    full_name: FullName = field(default=None)
    comment: Comment = field(default=None)
