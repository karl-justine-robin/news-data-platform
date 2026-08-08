class IncrementalResult:

    def __init__(
        self,
        new_articles,
        latest_watermarks,
    ):
        self.new_articles = new_articles
        self.latest_watermarks = latest_watermarks