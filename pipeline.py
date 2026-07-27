from src.framework.collector.collector import Collector


class Pipeline:

    def run(self):
        print("Starting pipeline...\n")

        collector = Collector()
        result = collector.collect()

        if result["status"] == "success":
            print("✓ Feed loaded successfully.")

        print("\nPipeline finished.")