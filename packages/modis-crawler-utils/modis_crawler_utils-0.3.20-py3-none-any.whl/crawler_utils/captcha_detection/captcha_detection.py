import re
import json
import logging
from urllib.parse import urljoin

from scrapy.crawler import Crawler
from scrapy.http import Request, Response


logger = logging.getLogger(__name__)


# Regular expression for checking if the given url is valid
url_regex = re.compile(  # from Django URLValidator
    r"^(?:http|ftp)s?://"  # http:// or https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


class CaptchaDetectionDownloaderMiddleware:
    """
        Captcha detection middleware for scrapy crawlers.
    It gets the HTML code from the response (if present), sends it to the captcha detection web-server
    and logs the result.

        If you don't want to check exact response if it has captcha, provide meta-key `dont_check_captcha`
    with `True` value.

        Middleware settings:
        * CAPTCHA_SERVICE_URL: str. For an example: http://127.0.0.1:8000
    """

    CAPTCHA_SERVICE_URL_SETTING = "CAPTCHA_SERVICE_URL"

    def __init__(self, captcha_service_url: str):
        global logger

        self.captcha_detection_endpoint = urljoin(
            captcha_service_url, "captcha_detector"
        )
        self.logger = logger

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        captcha_service_url = crawler.settings.get(cls.CAPTCHA_SERVICE_URL_SETTING)
        if captcha_service_url is None:
            raise ValueError("Captcha service URL setting is missing.")
        elif not isinstance(captcha_service_url, str):
            raise TypeError(
                f"{cls.CAPTCHA_SERVICE_URL_SETTING} must be a string, got {type(captcha_service_url)}"
            )
        else:
            if re.match(url_regex, captcha_service_url) is None:
                raise RuntimeError(f"{captcha_service_url} is not a valid URL.")
        return cls(captcha_service_url)

    @staticmethod
    def process_request(request, spider):
        return None

    def process_response(self, request: Request, response: Response, spider):
        if request.meta.get("dont_check_captcha", False):
            return response

        old_response = request.meta.get("__response_to_check_captcha", None)
        if old_response is None:  # response not from captcha-server
            return Request(
                url=self.captcha_detection_endpoint,
                method="POST",
                body=json.dumps({"html_page": response.text}),
                meta={"__response_to_check_captcha": response.replace(request=request)},
                callback=request.callback,
                cb_kwargs=request.cb_kwargs,
                errback=request.errback,
                dont_filter=True,
            )
        else:  # response from captcha-server
            if response.status != 200:
                self.logger.warning(f"The page {old_response.request} could not be processed by captcha-server")
            else:
                has_captcha = bool(json.loads(response.text)["has_captcha"])
                self.logger.info(
                    f"The page {old_response.request} {'has' if has_captcha else 'does not have'} captcha on the page.",
                )
            return old_response
