from common import models as m
from common.random import rand


class TestRegistration:

    def test_register(self, api):
        data = rand.object(m.RegisterReq)
        res = api.register_req(data).structure(m.RegisterRes)
        assert res.status_code == 200
        assert res.data.to_type(m.RegisterIntermediate) == data.to_type(m.RegisterIntermediate)
