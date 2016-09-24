# Crawler to scrape reviews from various e-commerce websites

How to run: If python and all the required python packages are installed, then go the directory containing the ".cfg" and run command "scrapy crawl <crawler name>". The <crawler name> can be found inside the spider files. For example, in case of amazon.com crawler, the crawler name is "amazoncom". So the command will be "scrapy crawl amazoncom" 

How does it work: First, the search item is taken as input. Then it is converted to the search link for the particular website. After that all the reviews of the first search result is extracted.

