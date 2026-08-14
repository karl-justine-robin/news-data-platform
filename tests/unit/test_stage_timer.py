from unittest.mock import patch

from src.framework.logging.stage_timer import (
    StageTimer,
)


def test_stage_timer_start():

    timer = StageTimer("TRANSFORM")

    with patch(
        "src.framework.logging.stage_timer.perf_counter",
        side_effect=[10.0],
    ):

        timer.start()

    assert timer.stage_name == "TRANSFORM"
    assert timer.start_time == 10.0


def test_stage_timer_finish():

    timer = StageTimer("TRANSFORM")

    with patch(
        "src.framework.logging.stage_timer.perf_counter",
        side_effect=[10.0, 12.5],
    ):

        timer.start()

        elapsed = timer.finish(
            articles=30,
        )

    assert elapsed == 2.5


def test_stage_timer_fail():

    timer = StageTimer("WAREHOUSE")

    with patch(
        "src.framework.logging.stage_timer.perf_counter",
        side_effect=[10.0, 11.25],
    ):

        timer.start()

        elapsed = timer.fail(
            "Database connection failed",
        )

    assert elapsed == 1.25


def test_stage_timer_finish_logs_duration(caplog):
    timer = StageTimer("TEST")

    with caplog.at_level("INFO"):
        timer.start()
        timer.finish()

    assert "[TEST] Starting" in caplog.text
    assert "[TEST] Completed" in caplog.text
    assert "duration=" in caplog.text

def test_stage_timer_records_stage_name():
    timer = StageTimer("COLLECT")

    assert timer.stage_name == "COLLECT"


