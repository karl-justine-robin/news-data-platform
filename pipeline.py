from src.framework.collector.collector import Collector
from src.framework.preprocessor.preprocessor import Preprocessor
from src.framework.transformer.transformer import Transformer
from src.framework.validator.validator import Validator
from src.framework.loader.loader import Loader



class Pipeline:

    def run(self):
        print("Starting pipeline...\n")

        # Collect
        collector = Collector()
        data = collector.collect()

        print(f"Feed Date : {data['feed_date']}")
        print(f"Timezone  : {data['timezone']}")
        print(f"Articles  : {len(data['items'])}\n")

        # Preprocess
        preprocessor = Preprocessor()
        data = preprocessor.preprocess(data)

        # Transform
        transformer = Transformer()
        articles = transformer.transform(data)

        # Validator
        validator = Validator()
        articles = validator.validate(articles)

        # Loader
        loader = Loader()
        loader.load(articles)

        print("\nStandardized Articles\n")

        for article in articles:
            print(article)

        print("\nPipeline finished.")