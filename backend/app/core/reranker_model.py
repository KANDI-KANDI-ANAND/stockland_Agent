class MockReranker:
    def predict(self, pairs):
        return [1.0] * len(pairs)
reranker = MockReranker()