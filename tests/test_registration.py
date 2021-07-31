from dataclasses import MISSING

import pendulum
import pytest

from common import models as m
from common.constants import ErrorMessages
from common.random import rand


class TestRegistration:

    def test_register(self, api):
        """Регистрация с заполнение всех полей"""
        data = rand.object(m.RegisterReq)
        creation_time = pendulum.now()
        res = api.register_req(data).structure(m.RegisterRes)
        assert res.status_code == 200
        assert res.data.to_type(m.RegisterIntermediate) == data.to_type(m.RegisterIntermediate)
        assert creation_time.diff(res.data.created_at).in_seconds() < 1
        assert res.data.updated_at is None

    def test_register_only_required(self, api):
        """Регистрация с заполнением только обязательных полей"""
        data = rand.partial(m.RegisterReq, use=["username", "password_hash", "email"])
        res = api.register_req(data).structure(m.RegisterRes)
        assert res.status_code == 200
        assert res.data.to_type(m.RegisterIntermediate) == data.to_type(m.RegisterIntermediate)

    @pytest.mark.parametrize("exclude_fields", [
        ["username"], ["password_hash"], ["email"], ["username", "password_hash", "email"]
    ])
    def test_register_missing_required(self, api, exclude_fields):
        """Регистрация с незаполненными обязательными полями"""
        data = rand.object(m.RegisterReq)
        for field in exclude_fields:
            setattr(data, field, MISSING)
        res = api.register_req(data).structure(m.ErrorRes)
        assert res.status_code == 422
        assert res.data.error == ErrorMessages.unprocessable_entity

    @pytest.mark.parametrize("value,status,error", [
        [None, 422, ErrorMessages.unprocessable_entity],
        ["", 400, ErrorMessages.errors_in_fields],
        ["12", 400, ErrorMessages.errors_in_fields],
    ])
    def test_register_incorrect_username(self, api, value, status, error):
        """Регистрация с недопустимым именем пользователя"""
        data = rand.object(m.RegisterReq)
        data.username = value
        res = api.register_req(data).structure(m.ErrorRes)
        assert res.status_code == status
        assert res.data.error == error.format("username")

    @pytest.mark.parametrize("value,status,error", [
        [None, 422, ErrorMessages.unprocessable_entity],
        ["", 400, ErrorMessages.errors_in_fields],
        ["example", 400, ErrorMessages.errors_in_fields],
        ["example@", 400, ErrorMessages.errors_in_fields],
        ["@example.com", 400, ErrorMessages.errors_in_fields],
        ["example@example.", 400, ErrorMessages.errors_in_fields],
    ])
    def test_register_incorrect_email(self, api, value, status, error):
        """Регистрация с недопустимым e-mail"""
        data = rand.object(m.RegisterReq)
        data.email = value
        res = api.register_req(data).structure(m.ErrorRes)
        assert res.status_code == status
        assert res.data.error == error.format("email")

    @pytest.mark.parametrize("value,status,error", [
        [None, 422, ErrorMessages.unprocessable_entity],
        ["", 400, ErrorMessages.errors_in_fields],
        ["a" * 7, 400, ErrorMessages.errors_in_fields],
    ])
    def test_register_incorrect_password(self, api, value, status, error):
        """Регистрация с недопустимым паролем"""
        data = rand.object(m.RegisterReq)
        data.password_hash = value
        res = api.register_req(data).structure(m.ErrorRes)
        assert res.status_code == status
        assert res.data.error == error.format("password_hash")

    @pytest.mark.parametrize("copy_fields", [
        ["username"], ["email"], ["email", "username"]
    ])
    def test_register_duplicate(self, api, copy_fields):
        """Регистрация с одинаковыми e-mail и именами пользователя"""
        data_1 = rand.object(m.RegisterReq)
        data_2 = rand.object(m.RegisterReq)
        for field in copy_fields:
            setattr(data_2, field, getattr(data_1, field))
        res = api.register_req(data_1).structure(m.RegisterRes)
        assert res.status_code == 200
        res = api.register_req(data_2).structure(m.ErrorRes)
        assert res.status_code == 400
        assert res.data.error == ErrorMessages.non_unique.format("unique_{}".format(copy_fields[0]))
