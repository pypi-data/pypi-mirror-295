# crawler-utils

Scrapy utils for Modis crawlers projects.

## MongoDB

Some utils connected with mongodb. 

MongoDBPipeline - pipeline for saving items in mongodb. 

Params:
* MONGODB_SERVER - address of mongodb database.
* MONGODB_PORT - port of mongodb database.
* MONGODB_DB - database where to save data.
* MONGODB_USERNAME - username for authentication in mongodb in MONGODB_DB database.
* MONGODB_PWD - password for authentication.
* DEFAULT_MONGODB_COLLECTION - default collection where to save data (default value is `test`).
* MONGODB_COLLECTION_KEY - key of item which identifies items collection name (`MONGO_COLLECTION`)
 where to save item (default value is `collection`).
* MONGODB_UNIQUE_KEY - key of item which identifies item
## Kafka

Some utils connected with kafka. 

KafkaPipeline - pipeline for pushing items into kafka.

Pipeline outputs data into stream with name `{RESOURCE_TAG}.{DATA_TYPE}`.
Where `RESOURCE_TAG` is tag of resource from which data is crawled and `DATA_TYPE` is type of 
data crawled: `data`, `post`, `comment`, `like`, `user`, `friend`, `share`, `member`, `news`, 
`community`.

 Params:
* KAFKA_ADDRESS - address of kafka broker.
* KAFKA_KEY - key of item which is put into kafka record key.
* KAFKA_RESOURCE_TAG_KEY - key of item which identifies item `RESOURCE_TAG` (default value is `platform`)
* KAFKA_DEFAULT_RESOURCE_TAG - default `RESOURCE_TAG` for crawled items without `KAFKA_RESOURCE_TAG_KEY` (default value is `crawler`)
* KAFKA_DATA_TYPE_KEY - key of item from which identifies item `DATA_TYPE` (default value is `type`).
* KAFKA_DEFAULT_DATA_TYPE - default `DATA_TYPE` for crawled items without `KAFKA_DATA_TYPE_KEY` (default value is `data`).
* KAFKA_COMPRESSION_TYPE - type of data compression in kafka for example `gzip`.

## CaptchaDetection

Captcha detection middleware for scrapy crawlers.
It gets the HTML code from the response (if present), sends it to the captcha detection web-server
and logs the result.

If you don't want to check exact response if it has captcha, provide meta-key `dont_check_captcha`
with `True` value.

The middleware must be set up with higher precedence (lower number) than RetryMiddleware:
```python
DOWNLOADER_MIDDLEWARES = {
    "crawler_utils.CaptchaDetectionDownloaderMiddleware": 549,  # By default, RetryMiddleware has 550
}
```

Middleware settings:
* CAPTCHA_SERVICE_URL: str. For an example: http://127.0.0.1:8000
