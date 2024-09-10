import asyncio
import gc
import json
import os
import re
import socket
import threading
import typing
from logging import Logger

import requests
from DrissionPage import ChromiumPage as DChromiumPage
from playwright.sync_api import Page, sync_playwright

logger = Logger(__name__)
thread_local = threading.local()


class ChromiumPage(DChromiumPage):

    def __new__(cls, addr_or_opts=None, tab_id=None, timeout=None):
        return super().__new__(cls, addr_or_opts, tab_id, timeout)

    def __init__(self, addr_or_opts=None, tab_id=None, timeout=None):
        super().__init__(addr_or_opts, tab_id, timeout)
        self.cdp_url = None

    def get_playwright_page(self):
        cdp_url = rbc.get_cdp_url_from_page(self)
        self.cdp_url = cdp_url
        browser = rbc.playwright_session.chromium.connect_over_cdp(cdp_url)
        page = browser.contexts[0].pages[-1]
        return page

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


class RemoteBrowserClient:
    _playwright_session = None

    def __init__(self):
        self.last_cdp_url = None
        self.browser_server_domain_host = os.environ.get('BROWSER_SERVER_HOST', '127.0.0.1:3000')
        self.browser_server_domain_host = '127.0.0.1:3000'
        domain, port = self.browser_server_domain_host.split(':')
        ip_host = socket.gethostbyname(domain)
        self.browser_server_ip_host = f'{ip_host}'
        self.browser_server_url = f'http://{self.browser_server_ip_host}:{port}'

    @property
    def playwright_session(self):
        playwright_session = getattr(thread_local, 'playwright_session', None)
        if not playwright_session:
            playwright_session = sync_playwright().start()
            # playwright_session.stop()
            setattr(thread_local, 'playwright_session', playwright_session)
        else:
            try:
                _loop = asyncio.get_running_loop()
                if _loop.is_running():
                    pass
                else:
                    raise
            except Exception:
                setattr(thread_local, 'playwright_session', None)
                return self.playwright_session

        return getattr(thread_local, 'playwright_session')



    def get_cdp_info(self, user_id=None, platform_id=None, bw_args=None):
        if bw_args is None:
            bw_args = []
        rq_url = self.browser_server_url + '/get_browser'
        bw_args.append('--window-size=1920,1080')

        # if self.headless:
        #     bw_args.append('--headless')

        rq_json = {
            'user_id': user_id or 'Default',
            'platform_id': platform_id or 'Default',
            'bw_args': bw_args,

        }

        rsp = requests.post(rq_url, json=rq_json)
        if not rsp.ok:
            logger.info(f"远程CDP出现错误, 请检查")
            raise
        bw_info = rsp.json()
        # data_id = bw_info['data_id']
        # url = bw_info['cdp_url']
        # post = bw_info['cdp_url']
        bw_info['cdp_url'] = bw_info['cdp_url'].replace('127.0.0.1', self.browser_server_ip_host)
        return bw_info

    def get_cdp_url(self, user_id=None, platform_id=None, bw_args=None):
        bw_info = self.get_cdp_info(user_id, platform_id, bw_args)
        return bw_info['cdp_url']

    def get_cdp_url_from_page(self, page: typing.Literal[Page, ChromiumPage]):
        if isinstance(page, ChromiumPage):
            r = page.browser.run_cdp('SystemInfo.getInfo')
        elif isinstance(page, Page):
            session = page.context.browser.new_browser_cdp_session()
            r = session.send('SystemInfo.getInfo')
        else:
            raise
        cmd_line = r['commandLine']
        transfer_port = re.search('--transfer_port=(\d+)', cmd_line).groups()[0]
        cdp_url = f'http://{rbc.browser_server_ip_host}:{transfer_port}'
        self.last_cdp_url = cdp_url
        return cdp_url

    def get_page(self, user_id=None, platform_id=None, bw_args=None, page_type='d'):
        cdp_url = self.get_cdp_url(user_id, platform_id, bw_args)
        if page_type == 'd':
            page = ChromiumPage(cdp_url)
            page = page.new_tab()
        elif page_type == 'p':
            browser = self.playwright_session.chromium.connect_over_cdp(cdp_url)
            page = browser.contexts[0].new_page()
        else:
            raise
        return page

    def release_page(self, page: typing.Literal[Page, ChromiumPage]):
        if isinstance(page, ChromiumPage):
            page.close()
            page.driver.stop()
        elif isinstance(page, Page):
            # thread_local = threading.local()
            page.close()
            # page.remove_listener('request')
            self.playwright_session.stop()

            bw = page.context.browser
            context = page.context
            del bw
            del context
            del page
            # delattr(thread_local, 'playwright_session')
        else:
            raise
        gc.collect()

    def to_drission_page(self, page: typing.Literal[Page, ChromiumPage]):
        cdp_url = self.get_cdp_url_from_page(page)
        new_page = ChromiumPage(cdp_url)
        new_page = new_page.get_tabs()[-1]
        return new_page

    def to_playwright_page(self, page: typing.Literal[Page, ChromiumPage]):
        cdp_url = self.get_cdp_url_from_page(page)
        browser = self.playwright_session.chromium.connect_over_cdp(cdp_url)
        page = browser.contexts[0].pages[-1]
        return page



if __name__ == '__main__':
    rbc = RemoteBrowserClient()

    page = rbc.get_page(page_type='p')
    page = rbc.get_page(page_type='p')
    page = rbc.get_page()
    tab_id = page.browser.tab_ids[-1]
    page: ChromiumPage = page.browser.page.get_tab(tab_id)
    page.refresh()
    page.run_cdp(
        "Debugger.enable",
    )
    page.run_cdp(
        "Debugger.disable",
    )

    location = page.run_cdp(
        "Debugger.setBreakpointByUrl",
        lineNumber=1,
        columnNumber=669514,
        # columnNumber=0,
        # columnNumber=1,
        urlRegex=r'main.d9858759.chunk.js',
    )
    script_id_list = [x['scriptId'] for x in location['locations']]
    location_list = location['locations']

    page.run_cdp(
        "Debugger.setBreakpointsActive",
        active=True,
    )
    page.run_cdp(
        "Debugger.getPossibleBreakpoints",
        start=location_list[1]
    )
    page.run_cdp(
        "Debugger.getPossibleBreakpoints",
    )
    page.run_cdp(
        "Debugger.pause",
    )
    page.run_cdp(
        "Debugger.resume",
    )


    def on_paused(*args, **kwargs):
        print(args, kwargs)


    page.driver.set_callback('Debugger.paused', on_paused)
    page.driver.set_callback('Debugger.paused', None)

    page.run_cdp(
        "Debugger.CallFrame",
    )

    for s_id in script_id_list:
        z = page.run_cdp(
            "Debugger.getScriptSource",
            scriptId=s_id,
        )
        src = z['scriptSource']
        if 'a.encryptSignV2' in src:
            print(s_id)
            print(src)

    js = """
    (0,
        a.encryptSignV2)({
            appKey: s.appKey,
            data: p,
            t: s.t,
            os: s.os,
            osv: s.osv,
            model: s.model,
            token: t
        })
    """
    page.run_cdp(
        "Debugger.evaluateOnCallFrame",
        callFrameId='495856556828576189.31.0',
        expression=js,
    )

    z = page.run_js(js)

    page.goto('https://www.baidu.com')
    rbc.release_page(page)
    page = rbc.get_page(page_type='p')
    page.goto('https://www.baidu.com')
    rbc.to_drission_page(page)
    r = page.xhr_request('GET', 'https://www.baidu.com', {}, {})

    page = rbc.to_playwright_page(page)
    page.goto('https://www.baidu.com')
    print(rbc.get_page())
