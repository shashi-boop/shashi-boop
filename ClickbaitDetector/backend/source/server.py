from flask import Flask, request, abort
import requests
import tldextract
from bs4 import BeautifulSoup
import json
from subprocess import check_output
from predict import predictor
from utils.get_news import get_news_from_headlines
from utils.similarity import Similarity

app = Flask(__name__)


@app.route("/", methods=["GET"])
def main_page():
    """
        - Handles incoming request from extension.
        - Retrieves URL from JSON and gets HTML content of page.
        - Cleans up HTML using Python Readability.
        - Sends headlines and summary to model.
    """
    url = request.args.get("url", None)
    headline = request.args.get("headline", None)

    if headline == None:
        if 'facebook' not in tldextract.extract(url).domain.lower():
            request_response = requests.get(url, allow_redirects=True)
            soup = BeautifulSoup(request_response.text, "lxml")
            headline = str(soup.title.string)

    percentage, similar_found = run_model(headline)

    if similar_found == None:
        response = app.response_class(
            response=json.dumps({"headline": headline, "percentage": percentage}),
            status=200,
            mimetype="application/json"
        )
    else:
        response = app.response_class(
            response=json.dumps({"headline": headline, "percentage": percentage, "similarArticles": similar_found}),
            status=200,
            mimetype="application/json"
        )
    return response


def run_model(headline):
    """
        - Run trained model on new article.
        - Passes headlines and summary to model.
    """
    # val = check_output("python source\predict.py \"{}\"".format(headline))
    # val = float(val.decode("utf8").replace("\r\n", ""))
    val = predictor.predict(headline)
    print("Percentage: " + str(val))
    if val > 70.0 or val < 30.0:
        return val, None
    else:
        similarity_score = compare_similar_news(headline)
        print(similarity_score)
        similar_articles_found = [i for i in similarity_score if i > 0.4].count(True) > 1
        return val, similar_articles_found


def compare_similar_news(headline):
    """
        - Calls utility function to get similar articles from Google News.
        - Compares news to check how similar the articles are.
        - Only used if clickabit detected percentage is low.
    """
    similar_articles = get_news_from_headlines(headline)
    similarity_score = Similarity().make_document(headline, similar_articles)
    return similarity_score


if __name__ == "__main__":
    app.run(port=5000, debug=True)
