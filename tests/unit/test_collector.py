import json
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from src.framework.collector.collector import Collector
from src.framework.error.exceptions import CollectorException


def test_collect_sample_data():

    collector = Collector()

    feeds = collector.collect()

    assert len(feeds) == 4

    sources = {feed["source"] for feed in feeds}

    assert sources == {
        "Bloomberg",
        "BusinessDesk",
        "CNBC",
        "Reuters",
    }


def test_collect_missing_file():

    with patch(
        "builtins.open",
        side_effect=FileNotFoundError,
    ):

        collector = Collector()

        with pytest.raises(CollectorException):
            collector.collect()


def test_collect_invalid_json():

    with patch(
        "builtins.open",
        mock_open(read_data="invalid json"),
    ), patch(
        "json.load",
        side_effect=json.JSONDecodeError(
            "Invalid JSON",
            "",
            0,
        ),
    ):

        collector = Collector()

        with pytest.raises(CollectorException):
            collector.collect()


def test_collect_empty_directory():

    with patch.object(
        Path,
        "glob",
        return_value=[],
    ):

        collector = Collector()

        feeds = collector.collect()

        assert feeds == []


def test_source_mapping():

    collector = Collector()

    feeds = collector.collect()

    expected = {
        "Bloomberg",
        "BusinessDesk",
        "CNBC",
        "Reuters",
    }

    actual = {
        feed["source"]
        for feed in feeds
    }

    assert actual == expected