from src.framework.collector.collector import Collector
from src.framework.preprocessor.preprocessor import Preprocessor


class Pipeline:

    def run(self):
        print("Starting pipeline...\n")

        collector = Collector()
        data = collector.collect()

        preprocessor = Preprocessor()
        data = preprocessor.preprocess(data)

        print("✓ Feed loaded successfully.\n")

        print(f"Feed Date : {data['feed_date']}")
        print(f"Timezone  : {data['timezone']}")
        print(f"Articles  : {len(data['items'])}")

        print("\nPipeline finished.")