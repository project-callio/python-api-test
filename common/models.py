from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from apitist import convclass
from apitist.decorators import transform
from apitist.random import Username, Email, str_type
from convclasses import mod
from pendulum import DateTime

Password = str_type("Password")
FullName = str_type("FullName")
Comment = str_type("Comment")


def _structure_uuid(uuid_string, _):
    """Structure hook for :class:`pendulum.DateTime`"""
    if isinstance(uuid_string, str):
        return UUID(uuid_string)
    else:
        return None


def _unstructure_uuid(uuid):
    if isinstance(uuid, UUID):
        return str(uuid)
    else:
        return None


convclass.register_hooks(UUID, _structure_uuid, _unstructure_uuid)


@dataclass
class ErrorRes:
    error: str


@transform
@dataclass
class RegisterReq:
    username: Username
    password_hash: Password
    email: Email
    full_name: FullName = field(default=None)
    comment: Comment = field(default=None)


@transform
@dataclass
class RegisterRes:
    id: UUID
    username: Username
    email: Email
    created_at: DateTime
    full_name: Optional[FullName] = field(default=None)
    comment: Optional[Comment] = field(default=None)
    updated_at: Optional[DateTime] = field(default=None)


@dataclass
class RegisterIntermediate:
    username: Username
    email: Email
    full_name: Optional[FullName] = field(default=None)
    comment: Optional[Comment] = field(default=None)
