import unittest
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from newspaper import Article
from main import vectorize_text, analyze_url


class TestMain(unittest.TestCase):
    # Text aquisition tests
    # ---------------------------------------------------------------------------------------------------------------------
    def test_text_aquisition(self):
        article_url = "https://www.dlcompare.com/gaming-news/animal-well-could-be-the-best-indie-game-of-the-year-42617"
        article = Article(article_url)
        article.download()
        article.parse()
        text = article.text
        self.assertTrue(len(text) > 0)

    def test_specific_text_aquisition(self):
        article_url = "https://www.dlcompare.com/gaming-news/animal-well-could-be-the-best-indie-game-of-the-year-42617"
        article = Article(article_url)
        article.download()
        article.parse()
        title = article.title
        self.assertEqual(title, "Animal Well could be the best indie game of the year")

    # SASAASASAS
    # ---------------------------------------------------------------------------------------------------------------------

    # Vectorize text tests
    # ---------------------------------------------------------------------------------------------------------------------
    def test_vectorize_text_with_english_stopwords(self):
        text = "This is a test sentence with some common English stopwords."
        vectorized_text = vectorize_text(text)
        for word in ["this", "is", "a", "with", "some"]:
            self.assertNotIn(word, vectorized_text)

    def test_vectorize_text_without_english_stopwords(self):
        text = "UniqueWord1 UniqueWord2 UniqueWord3"
        vectorized_text = vectorize_text(text)
        for word in ["uniqueword1", "uniqueword2", "uniqueword3"]:
            self.assertIn(word, vectorized_text)

    # Sentiment analysis tests
    # ---------------------------------------------------------------------------------------------------------------------

    def test_sentiment_analysis_positive(self):
        text = "Cute kitties are soft and fluffy."
        sid = SentimentIntensityAnalyzer()
        sentiment = sid.polarity_scores(text)
        self.assertGreater(sentiment["compound"], 0)

    def test_sentiment_analysis_negative(self):
        text = "I HATE spiders, they shoudnt have THAT many eyes!"
        sid = SentimentIntensityAnalyzer()
        sentiment = sid.polarity_scores(text)
        self.assertLess(sentiment["compound"], 0)

    # Results
    # ---------------------------------------------------------------------------------------------------------------------
    def test_analyze_produces_correct_result(self):
        url = "https://www.dlcompare.com/gaming-news/animal-well-could-be-the-best-indie-game-of-the-year-42617"
        analysis = analyze_url(url)
        self.assertIn("title", analysis)
        self.assertIn("sentiment", analysis)
        self.assertIn("score", analysis)
        self.assertIn("wordcloud", analysis)
        self.assertIn("article_url", analysis)

if __name__ == "__main__":
    unittest.main()
