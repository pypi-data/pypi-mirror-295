import json
from PlayDrissionPage.page_addition.listener import EventListener


class PagePlus:
    def __init__(self, instance):
        self._instance = instance
        self._over = EventListener(self._instance)

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        return instance

    def __getattr__(self, item):
        return getattr(self._instance, item)

    @property
    def over(self):
        return self._over

    def xhr_request(self, method,
                    url,
                    headers,
                    params,
                    post_query_mode=False,
                    with_credentials=False
                    ):
        # method = "GET"
        # url = "https://www.baidu.com"
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        # }
        # params = {}
        # post_query_mode = False
        # with_credentials = False
        request_txt = """
                        var method = "%(method)s";
                        var url = "%(url)s";
                        var headers = %(headers)s;
                        var params = %(params)s;
                        var post_query_format = %(post_query_format)s;
                        var xhr = new XMLHttpRequest();

                        if (%(with_credentials)s){
                            xhr.withCredentials = true;
                        };
                        xhr.open(method, url, false);

                        Object.keys(headers).forEach(function(key) {
                          xhr.setRequestHeader(key, headers[key]);
                        });

                        if (post_query_format){
                            data = new URLSearchParams(params);
                        } else {
                            data = JSON.stringify(params);
                        };

                        if (method == "GET") {
                            xhr.send();
                        } else if (method == "POST"){
                            xhr.send(data);
                        };
                        return xhr.responseText
                  """ % (
            {
                "method": method,
                "url": url,
                "headers": json.dumps(headers),
                "params": json.dumps(params),
                "post_query_format": 1 if post_query_mode else 0,
                "with_credentials": 1 if with_credentials else 0
            }
        )
        result = self.run_js(request_txt)
        return result

