#Crawler Script
### 1. Modify setting.yaml
### 2. Get all Article Links to Redis
`python arXivCrawler.py 1`
### 3. Get all Article Details to MySQL
`python arXivCrawler.py 2`

**Tips: You can execute this two scripts in different threads.**

For example, you can create a scheduled task to retrieve all links, while creating a monitoring task to monitor queue changes and automatically crawl all articles