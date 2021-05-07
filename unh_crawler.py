
import time
from urllib.parse import urljoin
import re
import requests
from indexer import storedata
from bs4 import BeautifulSoup
from jproperties import Properties
import threading
import time

base_url = "http://www.newhaven.edu/"
url_data = []
final_links = set()
index_name ="unh2"
es_url = "http://localhost:9200"


crawl_configs_dict = {}

crawl_all_pages = "false"

store_data_obj = None

def crawle_unh(url):
    global store_data_obj
    try:
        main_page_data = requests.get(url)
        soup = BeautifulSoup(main_page_data.text, 'html.parser')
        for x in soup.find_all('a'):
            temp_url = getValidUrl(x)
            if temp_url is not None:
                if temp_url not in final_links :
                    final_links.add(temp_url)
                    x = threading.Thread(target=store_data_obj.ingestDataFromUrl, args=(temp_url, index_name))
                    x.start()
                    time.sleep(0.002)
                    #store_data_obj.ingestDataFromUrl(temp_url, index_name)
                    if crawl_all_pages == "true" :
                        crawle_unh(temp_url)
    except Exception as e:
        print("error in reading link "+str(e))

    # got all urs now , get data from each one and store in elasticSearch
    print("final links size " +str(len(final_links)))



def create_index():
    global store_data_obj
    try:
        if store_data_obj is not None:
            print(index_name)
            store_data_obj.createIndex(index_name)
        #for link in final_links:

    except Exception as e:
        print("error occurred while storing data"+ str(e))



def getValidUrl(url):
    link = None
    try:
        temp = url.get('title')

        if temp is not None:
            data = url.get('href')
            link = urljoin('http://www.newhaven.edu/', data)
    except:
        print("url is not valid" +str(url))
    return link


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
        base_url = crawl_configs_dict["seed"]
        index_name = crawl_configs_dict["unh_index_name"]
        crawl_all_pages = crawl_configs_dict["crawl_all_pages"]
        print(" index name " + str(index_name))
        print(" crawling all pages "+str(crawl_all_pages))
        store_data_obj = storedata(es_url);
        create_index()
        crawle_unh(base_url)
        print(" crawling is done, now you can search over API")
    except Exception as e:
        print("Error "+str(e))
