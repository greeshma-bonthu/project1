from flask import Flask, request

from flask_cors import CORS
from elasticsearch import Elasticsearch
import requests
import json
from jproperties import Properties
app = Flask(__name__)
CORS(app)
es = Elasticsearch("http://localhost:9200")
index_name = "unh2"
crawl_configs_dict = {}

@app.route("/")
def welcome():
    return "Hello, welcome to UNH site, use http://localhost:5000/search?query=science for search results"


@app.route('/search', methods=['GET', 'POST'])
def search_request():
    query_param = request.args.get("query")
    print(query_param)
    if query_param is None:
        query_param = "*"
    from_param = request.args.get("offset")
    print(from_param)
    if from_param is None:
        from_param = 0
    size_param = request.args.get("per_page")
    print(size_param)
    if size_param is None:
        size_param = 10
    res = es.search(
        index=index_name,
        size=size_param,
        from_=from_param,
        body={
            "query": {
                "query_string": {
                    "fields": [
                        "url",
                        "title",
                        "meta_keywords",
                        "description",
                    ],
                    "query": query_param,
                    "default_operator": "OR",
                    "analyzer": "standard"
                }
            },
            "highlight": {
                "fields": {
                    "title": {
                        "pre_tags": [
                            "<strong>"
                        ],
                        "post_tags": [
                            "</strong>"
                        ],
                        "fragment_size": 150,
                        "number_of_fragments": 1,
                        "type": "plain"
                    },
                    "description": {
                        "pre_tags": [
                            "<strong>"
                        ],
                        "post_tags": [
                            "</strong>"
                        ],
                        "fragment_size": 150,
                        "number_of_fragments": 1,
                        "type": "plain"
                    }
                },
                "encoder": "html"
            }
        }
    )

    print(res)
    data = res
    return data

if __name__ == '__main__':
    try:
        configs = Properties()
        with open('crawler.properties', 'rb') as config_file:
            configs.load(config_file)

        crawl_configs_dict.clear()
        items_view = configs.items()
        for item in items_view:
            crawl_configs_dict[item[0]] = str(item[1].data)

        es_url = crawl_configs_dict["elastic_search_url"]
        print(es_url)
        index_name = crawl_configs_dict["search_index_name"]
        es = Elasticsearch(es_url)
        app.secret_key = 'mysecret'
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        print("exception "+str(e))

