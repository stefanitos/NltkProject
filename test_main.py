import unittest
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from main import (
    vectorize_text,
    analyze_url
)
import os
article_url = "https://www.dlcompare.com/gaming-news/animal-well-could-be-the-best-indie-game-of-the-year-42617"


class TestMain(unittest.TestCase):
    # Text aquisition tests
    # ---------------------------------------------------------------------------------------------------------------------
    def test_text_aquisition(self):
        """Test that the analyze_url function returns text from a valid URL."""
        text = analyze_url(article_url)["text"]
        self.assertGreater(len(text), 0)

    def test_specific_text_aquisition(self):
        title = analyze_url(article_url)["title"]
        self.assertEqual(title, "Animal Well could be the best indie game of the year")

    # Text processing techniques
    # ---------------------------------------------------------------------------------------------------------------------

    def test_text_processing_techniques(self):
        text = analyze_url(article_url)["text"]
        vectorized_text = vectorize_text(text)
        self.assertGreater(len(vectorized_text), 0)

    def test_specific_text_processing_techniques(self):
        text = analyze_url(article_url)["text"]
        vectorized_text = vectorize_text(text)
        self.assertNotIn("the", vectorized_text)

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
    def test_analyze_returns_error_message(self):
        url = "This is not a valid URL"
        analysis = analyze_url(url)
        self.assertEqual(analysis, "errrrm")

    def test_wordcloud_image_creation(self):
        analysis = analyze_url(article_url)
        wordcloud_file_path = analysis["wordcloud"]
        self.assertTrue(os.path.exists(wordcloud_file_path))

        if self._outcome.result.wasSuccessful():
            os.remove(wordcloud_file_path)


if __name__ == "__main__":
    unittest.main()
