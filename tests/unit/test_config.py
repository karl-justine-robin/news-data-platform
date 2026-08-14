import config


def test_validate_config_success(monkeypatch):
    monkeypatch.setattr(
        config,
        "DB_HOST",
        "localhost",
    )

    monkeypatch.setattr(
        config,
        "DB_NAME",
        "newsdb",
    )

    monkeypatch.setattr(
        config,
        "DB_USER",
        "postgres",
    )

    monkeypatch.setattr(
        config,
        "DB_PASSWORD",
        "postgres",
    )

    config.validate_config()


def test_validate_config_missing_values(monkeypatch):
    monkeypatch.setattr(
        config,
        "DB_HOST",
        None,
    )

    monkeypatch.setattr(
        config,
        "DB_NAME",
        "newsdb",
    )

    monkeypatch.setattr(
        config,
        "DB_USER",
        "postgres",
    )

    monkeypatch.setattr(
        config,
        "DB_PASSWORD",
        None,
    )

    try:
        config.validate_config()
    except RuntimeError as error:
        assert "DB_HOST" in str(error)
        assert "DB_PASSWORD" in str(error)
    else:
        raise AssertionError(
            "Expected RuntimeError"
        )


def test_get_bool_env_true(monkeypatch):
    monkeypatch.setenv(
        "TEST_BOOL",
        "true",
    )

    assert (
        config.get_bool_env("TEST_BOOL")
        is True
    )


def test_get_bool_env_false(monkeypatch):
    monkeypatch.setenv(
        "TEST_BOOL",
        "false",
    )

    assert (
        config.get_bool_env("TEST_BOOL")
        is False
    )


def test_get_bool_env_missing_uses_default(monkeypatch):
    monkeypatch.delenv(
        "TEST_BOOL",
        raising=False,
    )

    assert (
        config.get_bool_env("TEST_BOOL")
        is True
    )


def test_get_bool_env_missing_uses_false_default(monkeypatch):
    monkeypatch.delenv(
        "TEST_BOOL",
        raising=False,
    )

    assert (
        config.get_bool_env(
            "TEST_BOOL",
            default=False,
        )
        is False
    )


def test_pipeline_controls_can_be_disabled(monkeypatch):
    monkeypatch.setenv(
        "ENABLE_INCREMENTAL",
        "false",
    )
    monkeypatch.setenv(
        "ENABLE_BRONZE",
        "false",
    )
    monkeypatch.setenv(
        "ENABLE_SILVER",
        "false",
    )
    monkeypatch.setenv(
        "ENABLE_GOLD",
        "false",
    )
    monkeypatch.setenv(
        "ENABLE_WAREHOUSE",
        "false",
    )

    assert (
        config.get_bool_env("ENABLE_INCREMENTAL")
        is False
    )

    assert (
        config.get_bool_env("ENABLE_BRONZE")
        is False
    )

    assert (
        config.get_bool_env("ENABLE_SILVER")
        is False
    )

    assert (
        config.get_bool_env("ENABLE_GOLD")
        is False
    )

    assert (
        config.get_bool_env("ENABLE_WAREHOUSE")
        is False
    )


def test_pipeline_controls_can_be_enabled(monkeypatch):
    monkeypatch.setenv(
        "ENABLE_INCREMENTAL",
        "true",
    )
    monkeypatch.setenv(
        "ENABLE_BRONZE",
        "true",
    )
    monkeypatch.setenv(
        "ENABLE_SILVER",
        "true",
    )
    monkeypatch.setenv(
        "ENABLE_GOLD",
        "true",
    )
    monkeypatch.setenv(
        "ENABLE_WAREHOUSE",
        "true",
    )

    assert (
        config.get_bool_env("ENABLE_INCREMENTAL")
        is True
    )

    assert (
        config.get_bool_env("ENABLE_BRONZE")
        is True
    )

    assert (
        config.get_bool_env("ENABLE_SILVER")
        is True
    )

    assert (
        config.get_bool_env("ENABLE_GOLD")
        is True
    )

    assert (
        config.get_bool_env("ENABLE_WAREHOUSE")
        is True
    )


def test_pipeline_controls_default_to_true(monkeypatch):
    monkeypatch.delenv(
        "ENABLE_INCREMENTAL",
        raising=False,
    )
    monkeypatch.delenv(
        "ENABLE_BRONZE",
        raising=False,
    )
    monkeypatch.delenv(
        "ENABLE_SILVER",
        raising=False,
    )
    monkeypatch.delenv(
        "ENABLE_GOLD",
        raising=False,
    )
    monkeypatch.delenv(
        "ENABLE_WAREHOUSE",
        raising=False,
    )

    assert (
        config.get_bool_env("ENABLE_INCREMENTAL")
        is True
    )

    assert (
        config.get_bool_env("ENABLE_BRONZE")
        is True
    )

    assert (
        config.get_bool_env("ENABLE_SILVER")
        is True
    )

    assert (
        config.get_bool_env("ENABLE_GOLD")
        is True
    )

    assert (
        config.get_bool_env("ENABLE_WAREHOUSE")
        is True
    )


def test_pipeline_controls_accept_false(monkeypatch):
    monkeypatch.setenv(
        "ENABLE_INCREMENTAL",
        "false",
    )
    monkeypatch.setenv(
        "ENABLE_BRONZE",
        "false",
    )
    monkeypatch.setenv(
        "ENABLE_SILVER",
        "false",
    )
    monkeypatch.setenv(
        "ENABLE_GOLD",
        "false",
    )
    monkeypatch.setenv(
        "ENABLE_WAREHOUSE",
        "false",
    )

    assert (
        config.get_bool_env("ENABLE_INCREMENTAL")
        is False
    )

    assert (
        config.get_bool_env("ENABLE_BRONZE")
        is False
    )

    assert (
        config.get_bool_env("ENABLE_SILVER")
        is False
    )

    assert (
        config.get_bool_env("ENABLE_GOLD")
        is False
    )

    assert (
        config.get_bool_env("ENABLE_WAREHOUSE")
        is False
    )


def test_get_bool_env_invalid_value_raises(monkeypatch):
    monkeypatch.setenv(
        "TEST_BOOL",
        "invalid",
    )

    try:
        config.get_bool_env("TEST_BOOL")
    except ValueError:
        return

    raise AssertionError(
        "Expected ValueError for invalid boolean value"
    )