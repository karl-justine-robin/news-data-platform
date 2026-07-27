from src.framework.collector.collector import Collector


class Pipeline:

    def run(self):
        print("Starting pipeline...\n")

        collector = Collector()
        data = collector.collect()

        print(f"Feed Date : {data['feed_date']}")
        print(f"Timezone  : {data['timezone']}")
        print(f"Articles  : {len(data['items'])}")

        print("\nPipeline finished.")