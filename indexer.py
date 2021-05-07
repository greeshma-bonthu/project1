import os

import requests
from bs4 import BeautifulSoup
import time
from flask import Flask, render_template, request
from elasticsearch import Elasticsearch


class storedata:
    def __init__(self, url):
        self.url = url

        self.es_client = Elasticsearch([str(self.url)])

    def createIndex(self, index_name):
        setting = {
            "mappings": {
                "properties": {
                    "title": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    },
                    "url": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    },
                    "meta_keywords": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    },
                    "description": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    },

                    "created_date": {
                        "type": "date"
                    }
                }
            }
        }

        drop_index = self.es_client.indices.delete(index=index_name, ignore=[404])
        time.sleep(2)
        create_index = self.es_client.indices.create(index=index_name)
        self.es_client.indices.put_mapping(index=index_name, body=setting,ignore=400)
        # self.es_client.indices.put_mapping(index=index_name,body=mapping)

    def ingestDataFromUrl(self, url, index_name):
        try:

            page = requests.get(url).content
            soup = BeautifulSoup(page, 'lxml')
            title_name = ""
            temp_title_name = soup.find("meta", property="og:title")
            if temp_title_name is not None:
                title_name = soup.find("meta", property="og:title")["content"]
            keywords = ""
            temp_keywords = soup.find('meta', attrs={'name': 'Keywords'})

            if temp_keywords is not None:
                keywords = soup.find('meta', attrs={'name': 'Keywords'})["content"]
            description = ""
            temp_description = soup.find('meta', attrs={'name': 'Description'})
            if temp_description is not None:
                description = soup.find('meta', attrs={'name': 'Description'})["content"]

            # document for elasticsearch
            doc = {
                'created_date': time.strftime("%Y-%m-%d"),
                'title': title_name,
                'meta_keywords': keywords,
                'description': description,
                'url': url
            }

            print(doc)
            print(index_name)
            # ingest payload into elasticsearch
            res = self.es_client.index(index=index_name, doc_type="docs", body=doc)
        except Exception as e:
            print(" error storing data from " + str(e))

    def ingestDataFromFile(self, url, index_name):
        try:
            head, tail = os.path.split(url)
            title_name = tail
            description = ""
            with open(url) as f:
                description = f.readlines()

            # document for elasticsearch
            doc = {
                'date': time.strftime("%Y-%m-%d"),
                'title': title_name,
                'Keywords': head,
                'description': description,
                # appending as per  file URI scheme
                'url': "file:///" + url
            }

            print(doc)
            # ingest payload into elasticsearch
            res = self.es_client.index(index=index_name, doc_type="docs", body=doc)
        except Exception as e:
            print(" error storing data from " + str(e))
