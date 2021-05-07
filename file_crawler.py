import os
from indexer import storedata
from jproperties import Properties

dir_path = os.getcwd()  # "F:\python_work\pythonProject3\Data"

file_url = set()

index_name = "folder_data"

es_url = "http://localhost:9200"

crawl_configs_dict = {}


def crawle_dir(dir_name):
    print("file path "+dir_name)
    try:
        for dirName, subdirList, fileList in os.walk(dir_name):
            for fname in fileList:
                if fname.lower().endswith(('.txt', '.py')):
                    f_url = os.path.join(dirName, fname)
                    file_url.add(f_url)
    except Exception as e:
        print(e)

def store_dir_data(url_list):
    if len(url_list) > 0:
        try:
            store_data_obj = storedata(es_url);
            store_data_obj.createIndex(index_name)
            for link in url_list:
                store_data_obj.ingestDataFromFile(link, index_name)
        except Exception as e:
            print("error occurred while storing data" + str(e))


if __name__ == '__main__':
    print("File Traverse")
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
        dir_path = crawl_configs_dict["folder_seed"]
        index_name = crawl_configs_dict["folder_index_name"]
        crawle_dir(dir_path)
        store_dir_data(file_url)
    except Exception as e:
        print("exception "+str(e))
