import base64
import fnmatch
from collections.abc import Callable

from DrissionPage import ChromiumPage


class EventListener:
    def __init__(self, page: ChromiumPage):
        self.page = page
        self._request_patterns = []
        self._request_fun_dict = {}

    def event(self, **kwargs):
        pass

    def request(self, url):
        """
        Wildcards ('*' -> zero or more, '?' -> exactly one) are allowed. Escape character is backslash. Omitting is equivalent to "*".
        :param url:
        :return:
        """
        self._request_patterns.append({'urlPattern': url, 'requestStage': 'Request'})
        self.page.run_cdp('Fetch.enable', patterns=self._request_patterns)

        def wrapper(func):
            if not self._request_fun_dict:
                self.page._driver.set_callback('Fetch.requestPaused', self._request_event_fun)
            self._request_fun_dict[url] = func
            return func

        return wrapper

    def _request_event_fun(self, **kwargs):
        real_url = kwargs['request']['url']
        for url_pattern, func in self._request_fun_dict.items():
            if fnmatch.fnmatch(real_url, url_pattern):
                func(**kwargs)
                break

    def continue_request(self, **kwargs):
        """
        https://chromedevtools.github.io/devtools-protocol/tot/Fetch/#method-continueRequest
        RequestId
        An id the client received in requestPaused event.
        url
        string
        If set, the request url will be modified in a way that's not observable by page.
        method
        string
        If set, the request method is overridden.
        postData
        string
        If set, overrides the post data in the request. (Encoded as a base64 string when passed over JSON)
        headers
        array[ HeaderEntry ]
        If set, overrides the request headers. Note that the overrides do not extend to subsequent redirect hops, if a redirect happens. Another override may be applied to a different request produced by a redirect.
        interceptResponse
        boolean
        If set, overrides response interception behavior for this request. Experimental
        :param kwargs:
        :return:
        """
        _kwargs = {}
        if 'requestId' in kwargs:
            _kwargs['requestId'] = kwargs['requestId']
        if 'url' in kwargs:
            _kwargs['url'] = kwargs['url']
        if 'method' in kwargs:
            _kwargs['method'] = kwargs['method']
        if 'postData' in kwargs:
            post_data = kwargs['postData']
            _kwargs['postData'] = base64.b64encode(post_data.encode()).decode()
        if 'headers' in kwargs:
            headers = kwargs['headers']
            _kwargs['headers'] = [{"name": key, "value": value} for key, value in headers.items()]
        if 'interceptResponse' in kwargs:
            _kwargs['interceptResponse'] = kwargs['interceptResponse']

        self.page.run_cdp('Fetch.continueRequest', **_kwargs)

    def fail_request(self, requestId, errorReason='ConnectionClosed'):
        """
        https://chromedevtools.github.io/devtools-protocol/tot/Fetch/#method-failRequest
        RequestId
        An id the client received in requestPaused event.
        errorReason
        string
        Causes the request to fail with the given reason.
        Network level fetch failure reason.
        Allowed Values: Failed, Aborted, TimedOut, AccessDenied, ConnectionClosed, ConnectionReset, ConnectionRefused, ConnectionAborted, ConnectionFailed, NameNotResolved, InternetDisconnected, AddressUnreachable, BlockedByClient, BlockedByResponse
        :param kwargs:
        :return:
        """
        _kwargs = {'requestId': requestId, 'errorReason': errorReason}
        self.page.run_cdp('Fetch.failRequest', **_kwargs)

    def disable_request(self, url: [Callable, str, None] = None):
        if isinstance(url, Callable):
            self._request_patterns = [x for x in self._request_patterns if url(x['urlPattern'])]
        elif isinstance(url, str):
            self._request_patterns = [x for x in self._request_patterns if x['urlPattern'] != url]
        elif url is None:
            self._request_patterns = []
        else:
            raise TypeError
        if not self._request_patterns or not url:
            self.page.run_cdp('Fetch.disable')
        else:
            self.page.run_cdp('Fetch.enable', patterns=self._request_patterns)
        return True

    def response(self, **kwargs):
        pass
