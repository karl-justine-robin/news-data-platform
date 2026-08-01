class PipelineException(Exception):
    """Base exception for the News Data Platform."""


class CollectorException(PipelineException):
    """Raised when data collection fails."""


class PreprocessorException(PipelineException):
    """Raised when preprocessing fails."""


class TransformerException(PipelineException):
    """Raised when transformation fails."""


class ValidatorException(PipelineException):
    """Raised when validation fails."""


class LoaderException(PipelineException):
    """Raised when loading data fails."""