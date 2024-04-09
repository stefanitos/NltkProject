import random
from newspaper import Article
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    url = request.json["url"]
    article = Article(url)
    article.download()
    article.parse()
    text = article.text
    sid = SentimentIntensityAnalyzer()
    sentiment = sid.polarity_scores(text)
    analysis = {
        "title": article.title,
        "sentiment": (
            "positive"
            if sentiment["compound"] > 0
            else "negative" if sentiment["compound"] < 0 else "neutral"
        ),
        "score": sentiment["compound"],
    }
    return jsonify(analysis)


if __name__ == "__main__":
    app.run(debug=True)
