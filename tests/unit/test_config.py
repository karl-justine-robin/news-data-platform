import config


def test_validate_config_success(monkeypatch):
    monkeypatch.setattr(config, "DB_HOST", "localhost")
    monkeypatch.setattr(config, "DB_NAME", "newsdb")
    monkeypatch.setattr(config, "DB_USER", "postgres")
    monkeypatch.setattr(config, "DB_PASSWORD", "postgres")

    config.validate_config()


def test_validate_config_missing_values(monkeypatch):
    monkeypatch.setattr(config, "DB_HOST", None)
    monkeypatch.setattr(config, "DB_NAME", "newsdb")
    monkeypatch.setattr(config, "DB_USER", "postgres")
    monkeypatch.setattr(config, "DB_PASSWORD", None)

    try:
        config.validate_config()
    except RuntimeError as error:
        assert "DB_HOST" in str(error)
        assert "DB_PASSWORD" in str(error)
    else:
        raise AssertionError(
            "Expected RuntimeError"
        )