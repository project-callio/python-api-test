import pendulum

from common import models as m
from common.random import rand


class TestRegistration:

    def test_register(self, api):
        data = rand.object(m.RegisterReq)
        creation_time = pendulum.now()
        res = api.register_req(data).structure(m.RegisterRes)
        assert res.status_code == 200
        assert res.data.to_type(m.RegisterIntermediate) == data.to_type(m.RegisterIntermediate)
        assert creation_time.diff(res.data.created_at).in_seconds() < 1
        assert res.data.updated_at is None
