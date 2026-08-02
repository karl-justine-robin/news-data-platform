from src.framework.collector.collector import Collector
from src.framework.preprocessor.preprocessor import Preprocessor
from src.framework.schema.schema_validator import SchemaValidator
from src.framework.transformer.transformer import Transformer
from src.framework.validator.validator import Validator


def test_pipeline_integration():

    collector = Collector()
    schema_validator = SchemaValidator()
    preprocessor = Preprocessor()
    transformer = Transformer()
    validator = Validator()

    # Collect
    feeds = collector.collect()

    assert len(feeds) == 4

    # Validate vendor schemas
    schema_validator.validate(feeds)

    # Preprocess
    processed_feeds = preprocessor.preprocess(feeds)

    assert len(processed_feeds) == 4

    # Transform
    articles = transformer.transform(processed_feeds)

    assert len(articles) == 30

    # Validate business rules
    validated_articles = validator.validate(articles)

    assert len(validated_articles) == 30