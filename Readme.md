
# UNH Crawler

This project is used to crawl all the pages from UNH site http://newhaven.edu/search/ and store in db and can use for searching.

Sowftwares used :

1. Python
2. Elasticsearch

## Instalation

##### Python and dependent module steps:
- Download and install python 3.9.X from "https://www.python.org/downloads/"
- Check installtion status using "python -v" command in command prompt
- Install pip from "https://phoenixnap.com/kb/install-pip-windows"
- Install all dependecy modules using "pip install 'module name'" syntax, below are required examples, it will ignore if module already exists.
		- pip install requests
		- pip install bs4
		- pip install jproperties
		- pip install flask
		- pip install elasticsearch
		- pip install flask_paginate
- Incase if you see any error like "*Module Not found*" which is not listed above then, please install that module using pip command
		- pip install module_name

##### Elastic Search Instalation:

- Install the latest java version or check your current version by using “java -version” command in command line prompt (Java version should be 8 or more)
- Set environment variable for JAVA
- Download elastic zip file from "https://www.elastic.co/downloads/elasticsearch"
- Unzip the file
- Go to bin folder
- Double click on “elasticsearch.bat” file
- Open a browser, type “*localhost:9200*” and it will show you name, cluster name of elasticsearch and other information in JSON format.
					{
					  "name" : "LAPTOP-1234567",
					  "cluster_name" : "elasticsearch",
					  "cluster_uuid" : "XggqxXAhSgW8scTOBgiyHg",
					  "version" : {
						"number" : "7.12.1",
						"build_flavor" : "default",
						"build_type" : "zip",
						"build_hash" : "3186837139b9c6b6d23c3200870651f10d3343b7",
						"build_date" : "2021-04-20T20:56:39.040728659Z",
						"build_snapshot" : false,
						"lucene_version" : "8.8.0",
						"minimum_wire_compatibility_version" : "6.8.0",
						"minimum_index_compatibility_version" : "6.0.0-beta1"
					  },
					  "tagline" : "You Know, for Search"
					}

## run 

### run unh crawler
	- Once installation of all modules is done, we can run our crawler program, which can crawl all pages and index the data into elastic search.
	- Before running, we can edit crawler.properties file to configure like elastic_search url, index name, base url etc. if you don't edit anything it will used default properties
			- seed = http://www.newhaven.edu/ 	 			- base url to start crawl
			- unh_index_name = unh  			 			- index name to store in elasticsearch
			- elastic_search_url = http://localhost:9200	- configure elastic search server url details
			-crawl_all_pages = false						- since it takes sometime (depends on internet and system spead) to crawl all pages, to make execution fast it read few 												 pages and index them to search. If you would like to crawl all pages, please change to true.
			
#command#
		open command prompt and run "*python unh_crawler.py*" from current directory where project1 source code is available. 

## File Crawler

	- This is used to crawl all the text files (for now implemented for .txt and .py file) in given folder and index them into elastic search
		
### run file crawler (traverser)
	- Before running, we can edit crawler.properties file to configure like elastic_search url, index name,folder_seed etc. 
			- folder_seed = F://python_work//pythonProject3//Data  	- base folder, to crawl the sub folders and files to read content and index them.
			- folder_index_name = folder_data						- index name to store in elastic search

#command#
		Open command prompt and run "*python file_crawler.py*" from current directory where project1 source code is available. 
		
### run search api

	- Once unh crawlling is done using above unh_crawler program, now we can start backend server to search on stored content.
	- Before running, we can edit crawler.properties file to configure like elastic_search url, index name (this is same file edited above, now add for search index name)
	
		-search_index_name = unh						- index to be searched when given query, if you created multiple indexes (like using file crawler), then you can pass unh, unh2 to search on both

#command#
	- Open command prompt and run "*python app_search.py*" from current directory where project1 source code is available. 
	- Once the server started, it will show console like below on command prompt
				 * Serving Flask app "app_search" (lazy loading)
				 * Environment: production
				   WARNING: This is a development server. Do not use it in a production deployment.
				   Use a production WSGI server instead.
				 * Debug mode: off
				 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
	- If you see above screen, now you can use any rest client like postman/ browser ro search query
	- Open any browser and type *"http://localhost:5000/"* then it will show wel come message
				Hello, welcome to UNH site, use http://localhost:5000/search?query=science for search results
	- you can use http://localhost:5000/search?query=science for searching results where *science* is a keyword, you can use any key word for searching purpose
	- you can use *per_page* param to limit the number of records per search like http://localhost:5000/search?query=science&per_page=2
	###understading response format###
	
			*sample response*
					{"_shards":{"failed":0,"skipped":0,"successful":1,"total":1},"hits":{"hits":[{"_id":"tiMuPnkBpu59E7P0iYFk","_index":"unh","_score":6.5562696,"_source":{"meta_keywords":"","date":"2021-05-06","description":"","title":"Science","url":"https://issuu.com/categories/science?issuu_product=footer&issuu_subproduct=explore&issuu_context=link"},"_type":"docs","highlight":{"title":["<strong>Science</strong>"]}},{"_id":"tyMuPnkBpu59E7P0kYGg","_index":"unh","_score":5.86443,"_source":{"meta_keywords":"University of New Haven","date":"2021-05-06","description":"404 - Page Not Found","title":" - University of New Haven","url":"http://www.newhaven.edu/categories/science"},"_type":"docs"}],"max_score":6.5562696,"total":{"relation":"eq","value":48}},"timed_out":false,"took":442}
				- "total":{"relation":"eq","value":48} indicates total matches found in search query, in this case 48 matches found but returned first 2 pages
				- "took":442 indicates 442 milli seconds to search query and return results
			
	- you can use *offset* param to start the records fetching from like http://localhost:5000/search?query=science&per_page=2&offset=5 which returns records from 5 and 2 records   per page
	
	

# Data Storage Analysis

	- After inspecting multiple times UNH site using before crawling, I observed that most of search related information is stored in page properties like "tile, keywords, url and description". These fields mostly match when we search with keywords and a sample page crawled information looks like below
	
		{'date': '2021-05-06', 'title': 'Charging into Fall 2021  - University of New Haven', 'Keywords': 'Charging into Fall 2021, fall 2021 semester, COVID-19, planning', 'description': 'The University of New Haven has long prided itself on being prepared for all eventualities – and instilling that mindset in our students. That’s why we have been as successful as any institution in protecting our University community throughout the COVID-19 pandemic, mitigating the impact of the virus, and continuing to provide a meaningful and rewarding educational experience in and out of the classroom for our students. This is a significant point of pride for the University, and it is a credit to everyone in our community. ', 'url': 'http://www.newhaven.edu/fall2021/index.php'}

	- An average 3 kb data is required per page, total there are ~26,100 pages and we required  78300 KB. This storage is only to store above fields content not for any images or videos or other data available on UNH site.
	- For file crawler, the storage really depends on content stored in file.
	- Since we may recreate indexes or store crawled data on multiple indexes, we required a data store which can be really scalable and distributed (which is covered in **Data store Analysis**).


# Data store Analysis
		
	- Before finalizing the database to store, I have analyzed following noSQL DB's which can support both noSQL type 
	  document based and distributed (For scaling purpose).

	1. Elasticsearch
	2. MongoDB  
	3. Apache Solr

	After going through each one above DB features, I have filtered  Elasticsearch and Apache Solr for storing 
	crawled information. 

	The main reason behind this is, as we are trying to build a search engine, and we need a database which primary 
	database model is search engine. where as mongob supports Primary database model as document store.

	**Elasticsearch**                                               **Solr**  
	A distributed, RESTful modern search                            A widely used distributed, scalable 
	and analytics engine based on Apache Lucene info                search engine based on Apache Lucene

	*Score*	155.35 Rank	#8 Overall # 1Search engines                Score	51.19 Rank	#20 Overall  #3Search engines

	SQL-like query language                                         Solr Parallel SQL Interface

	*Configuration*
	In ElasticSearch, the configuration is done in                  In Solr, the configuration of all components
	elasticsearch.yml file                                          is defined in the solrconfig.xml file 
	Many settings exposed by ElasticSearch can be                   and after each change, restart, or reload of Solr node, 
	changed on the live cluster for which the                       it is needed.
	ElasticSearch nodes don’t require a restart.

	*Shard Rebalancing*

	As you add new machines,                                        automatic shard rebalancing behavior does not exist in Solr
	ElasticSearch will automatically load 
	balance and move shards to new nodes in the cluster
	

	Solr is search server for creating standard search applications, no massive indexing and no real time updates are required,
	but on the other hand Elasticsearch takes it to the next level with an architecture aimed at building modern real-time
	search applications. Percolation is an exciting and innovative feature. Elasticsearch is scalable and speedy, 
	and if distributed indexing is needed then Elasticsearch would be the right choice.

	References
	https://sematext.com/blog/2012/08/23/solr-vs-elasticsearch-part-1-overview/> 
	http://www.datanami.com/2015/01/22/solr-elasticsearch-question/
	https://en.wikipedia.org/wiki/Elasticsearch
	https://dzone.com/articles/solr-vs-elasticsearch

	Considering above features, differences and support, for a new search engine to develop  I feel Elastic Search 
	would be better choice and consider the same for this project