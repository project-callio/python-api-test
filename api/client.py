from dataclasses import dataclass, field

from apitist import (
    PrepRequestInfoLoggingHook,
    RequestDataclassConverterHook,
    ResponseDataclassConverterHook,
    ResponseInfoLoggingHook,
    Session,
    session,
)
from apitist.decorators import get

from common import models as m


def init_session(base_url: str = None):
    s = session(base_url)
    s.add_hook(PrepRequestInfoLoggingHook)
    s.add_hook(ResponseInfoLoggingHook)
    s.add_hook(RequestDataclassConverterHook)
    s.add_hook(ResponseDataclassConverterHook)
    return s


@dataclass
class Client:
    host: str
    session: Session = field(init=False)

    def __post_init__(self):
        self.session = init_session(self.host)

