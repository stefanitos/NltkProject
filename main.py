import os
from newspaper import Article, Config
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask import Flask, request, jsonify, render_template
import json
import matplotlib

matplotlib.use("agg")

app = Flask(__name__)
user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
)
config = Config()
config.browser_user_agent = user_agent
config.request_timeout = 10


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    url = request.json["url"]
    article = Article(url, config=config)
    article.download()
    article.parse()
    text = article.text
    title = article.title
    sid = SentimentIntensityAnalyzer()
    sentiment = sid.polarity_scores(text)
    plot_url = generate_wordcloud(text, title)

    analysis_file_path = os.path.join("static", "analysis.json")
    analysis = {
        "title": title,
        "sentiment": (
            "positive"
            if sentiment["compound"] > 0
            else "negative" if sentiment["compound"] < 0 else "neutral"
        ),
        "score": sentiment["compound"],
        "wordcloud": plot_url,
        "article_url": url,
    }

    existing_analyses = get_analysis()
    existing_analyses.append(analysis)

    with open(analysis_file_path, "w") as f:
        json.dump(existing_analyses, f)

    return jsonify(analysis)


def get_analysis():
    analysis_file_path = os.path.join("static", "analysis.json")
    if os.path.exists(analysis_file_path):
        with open(analysis_file_path, "r") as f:
            return json.load(f)
    else:
        return []


def generate_wordcloud(text, title=None):
    """Generates a wordcloud from the given text and saves it to a file."""
    vectorizer = TfidfVectorizer()
    english_stopwords = set(stopwords.words("english"))
    print(english_stopwords)
    words = word_tokenize(text)
    words = [word for word in words if word.lower() not in english_stopwords]
    X = vectorizer.fit_transform(words)
    wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(
        dict(zip(vectorizer.get_feature_names_out(), X.sum(axis=0).A1))
    )

    wordcloud_dir = "static/wordclouds"
    if not os.path.exists(wordcloud_dir):
        os.makedirs(wordcloud_dir)

    # Using the title as the filename
    filename = f"{hash(title)}-wordcloud.png"
    filepath = os.path.join(wordcloud_dir, filename)
    wordcloud.to_file(filepath)

    return f"/static/wordclouds/{filename}"


if __name__ == "__main__":
    app.run(debug=True)
