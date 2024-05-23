import os
from newspaper import Article, Config, ArticleException
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)
user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
)
config = Config()
config.browser_user_agent = user_agent
config.request_timeout = 10
analysis_file_path = os.path.join("static", "analysis.json")


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    url = request.json["url"]
    analysis = analyze_url(url)

    save_analysis(analysis)  # Save the analysis to JSON file

    return jsonify(analysis)


def analyze_url(url):
    article = Article(url, config=config)
    try:
        article.download()
        article.parse()
    except ArticleException:
        return "errrrm"

    text = article.text
    title = article.title
    sid = SentimentIntensityAnalyzer()
    sentiment = sid.polarity_scores(text)
    wordcloud_url = generate_wordcloud(text, title)

    analysis = {
        "title": title,
        "sentiment": (
            "positive"
            if sentiment["compound"] > 0
            else "negative" if sentiment["compound"] < 0 else "neutral"
        ),
        "score": sentiment["compound"],
        "wordcloud": wordcloud_url,
        "article_url": url,
        "text": text,
    }

    return analysis


def save_analysis(analysis):
    existing_analyses = get_analysis()
    existing_analyses.append(analysis)

    with open(analysis_file_path, "w") as f:
        json.dump(existing_analyses, f)


def get_analysis():
    if os.path.exists(analysis_file_path):
        with open(analysis_file_path, "r") as f:
            return json.load(f)
    else:
        return []


def vectorize_text(text):
    vectorizer = TfidfVectorizer()
    english_stopwords = stopwords.words("english")
    words = word_tokenize(text)
    words = [word for word in words if word.lower() not in english_stopwords]
    X = vectorizer.fit_transform(words)
    return dict(zip(vectorizer.get_feature_names_out(), X.sum(axis=0).A1))


def generate_wordcloud(text, title=None):
    """Generates a wordcloud of the most common words in the text. Returns the URL of the generated wordcloud image."""
    wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(
        vectorize_text(text)
    )

    wordcloud_dir = "static/wordclouds"
    if not os.path.exists(wordcloud_dir):
        os.makedirs(wordcloud_dir)

    filename = "".join(e for e in title if e.isalnum())[:25] + ".png"
    filepath = os.path.join(wordcloud_dir, filename)
    wordcloud.to_file(filepath)

    return f"static/wordclouds/{filename}"


if __name__ == "__main__":
    app.run(debug=True)
