# Downloader server

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from image_downloader.layer.download import GoogleURLCrawler
from image_downloader.layer.llm import Critic

from image_downloader.pipeline import Pipeline

import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

pipeline = Pipeline(
    crawlers=[GoogleURLCrawler()],
    layers=[
        Critic(
            base_url=os.environ["BASE_URL"],
            api_key=os.environ["API_KEY"],
            model="gpt-4o",
            sys_prompt="Now, I will present you with some image-text pairs. If they correctly correspond, respond with \"YES\"; otherwise, reply with \"NO\".",
            filter_func=lambda resp: "YES" in resp
        )
    ]
)

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    try:
        urls = pipeline(
            query=data["query"],
            text=data["text"],
            max_n=data.get("max_n", 10)
        )
        return jsonify(urls), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7077)