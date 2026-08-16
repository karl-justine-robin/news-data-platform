from unittest.mock import MagicMock, patch

from src.framework.repository.pipeline_run_repository import (
    PipelineRunRepository,
)


def test_finish_run_returns_when_run_does_not_exist():

    repository = PipelineRunRepository()

    connection = MagicMock()
    cursor = MagicMock()
    cursor.fetchone.return_value = None

    cursor_context = MagicMock()
    cursor_context.__enter__.return_value = cursor
    connection.cursor.return_value = cursor_context

    connection_context = MagicMock()
    connection_context.__enter__.return_value = connection

    with patch(
        "src.framework.repository.pipeline_run_repository.psycopg.connect",
        return_value=connection_context,
    ):

        result = repository.finish_run(
            run_id=999,
            success=True,
            records_processed=10,
        )

    assert result is None

    cursor.execute.assert_called_once()

    connection.commit.assert_not_called()