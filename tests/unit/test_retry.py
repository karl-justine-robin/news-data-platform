from unittest.mock import Mock, call, patch

import pytest

from src.framework.error.retry import retry


def test_retry_returns_result_without_retrying_on_success():

    func = Mock(return_value="success")

    result = retry(
        func,
        max_attempts=3,
    )

    assert result == "success"
    assert func.call_count == 1


def test_retry_succeeds_after_transient_failure():

    func = Mock(
        side_effect=[
            RuntimeError("Temporary failure"),
            "success",
        ]
    )

    with patch(
        "src.framework.error.retry.time.sleep"
    ) as sleep:

        result = retry(
            func,
            max_attempts=3,
            delay=2,
        )

    assert result == "success"
    assert func.call_count == 2
    sleep.assert_called_once_with(2)


def test_retry_raises_after_max_attempts():

    error = RuntimeError("Permanent failure")

    def failing_function():
        raise error

    with patch(
        "src.framework.error.retry.time.sleep"
    ) as sleep:

        with pytest.raises(RuntimeError) as exc_info:

            retry(
                failing_function,
                max_attempts=3,
                delay=2,
            )

    assert exc_info.value is error
    assert sleep.call_count == 2


def test_retry_respects_custom_max_attempts():

    error = RuntimeError("Temporary failure")

    def failing_function():
        raise error

    with patch(
        "src.framework.error.retry.time.sleep"
    ) as sleep:

        with pytest.raises(RuntimeError):

            retry(
                failing_function,
                max_attempts=5,
                delay=1,
            )

    sleep.assert_has_calls(
        [
            call(1),
            call(1),
            call(1),
            call(1),
        ]
    )
    assert sleep.call_count == 4


def test_retry_only_catches_configured_exceptions():

    error = ValueError("Do not retry")

    def failing_function():
        raise error

    with patch(
        "src.framework.error.retry.time.sleep"
    ) as sleep:

        with pytest.raises(ValueError) as exc_info:

            retry(
                failing_function,
                max_attempts=3,
                delay=1,
                exceptions=(RuntimeError,),
            )

    assert exc_info.value is error
    sleep.assert_not_called()


def test_retry_logs_failed_attempt(caplog):

    def failing_function():
        raise RuntimeError("Temporary failure")

    with patch(
        "src.framework.error.retry.time.sleep"
    ):

        with pytest.raises(RuntimeError):

            retry(
                failing_function,
                max_attempts=2,
                delay=1,
            )

    assert "Attempt 1/2 failed: Temporary failure" in caplog.text
    assert "Attempt 2/2 failed: Temporary failure" in caplog.text


def test_retry_logs_maximum_attempts_reached(caplog):

    def failing_function():
        raise RuntimeError("Permanent failure")

    with patch(
        "src.framework.error.retry.time.sleep"
    ):

        with pytest.raises(RuntimeError):

            retry(
                failing_function,
                max_attempts=2,
                delay=1,
            )

    assert (
        "Maximum retry attempts reached for failing_function"
        in caplog.text
    )