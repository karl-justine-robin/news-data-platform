import json
from config import SAMPLE_FEED


class Collector:

    def collect(self):
        print("Collecting data from BusinessDesk...")

        with open(SAMPLE_FEED, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data