from common import models as m


class TestRegistration:

    def test_register(self, api):
        data = m.RegisterReq(
            "example_user",
            "example_pass",
            "example@example.com",
            "Example User",
            "Example comment"
        )
        res = api.register_req(data)
        assert res.status_code == 200
