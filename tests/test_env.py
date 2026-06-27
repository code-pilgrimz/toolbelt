import os
from toolbelt.env import env, env_bool


def test_env_cast(monkeypatch):
    monkeypatch.setenv("PORT", "8080")
    assert env("PORT", cast=int) == 8080


def test_env_bool(monkeypatch):
    monkeypatch.setenv("DEBUG", "yes")
    assert env_bool("DEBUG") is True
    assert env_bool("MISSING", default=False) is False
