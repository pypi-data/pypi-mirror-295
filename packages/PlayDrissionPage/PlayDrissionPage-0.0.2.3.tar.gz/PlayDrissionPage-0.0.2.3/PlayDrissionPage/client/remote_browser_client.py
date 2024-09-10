import asyncio
import gc
import os
import re
import socket
import threading
import typing
from logging import Logger

import requests
from DrissionPage import ChromiumPage
from playwright.sync_api import Page, sync_playwright

from PlayDrissionPage.page_addition.page_plus import PagePlus

ChromiumPagePlus = typing.Union[PagePlus, ChromiumPage]

logger = Logger(__name__)
thread_local = threading.local()


class RemoteBrowserClient:

    def __init__(self):
        self.last_cdp_url = None
        self.browser_server_domain_host = os.environ.get('BROWSER_SERVER_HOST_PORTS', '127.0.0.1:3000')

    @property
    def browser_server_ip_host(self):
        domain, _ = self.browser_server_domain_host.split(':')
        ip_host = socket.gethostbyname(domain)
        return f'{ip_host}'

    @property
    def browser_server_post(self):
        _, port = self.browser_server_domain_host.split(':')
        return port

    @property
    def browser_server_url(self):
        return f'http://{self.browser_server_ip_host}:{self.browser_server_post}'

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
        cdp_url = f'http://{self.browser_server_ip_host}:{transfer_port}'
        self.last_cdp_url = cdp_url
        return cdp_url

    @classmethod
    def inject_plus(cls, page) -> ChromiumPagePlus:
        page = PagePlus(page)
        page = typing.cast(ChromiumPagePlus, page)
        return page

    def get_d_page(self, user_id=None, platform_id=None, bw_args=None):
        cdp_url = self.get_cdp_url(user_id, platform_id, bw_args)
        page = ChromiumPage(cdp_url).new_tab()
        page = self.inject_plus(page)
        return page

    def get_p_page(self, user_id=None, platform_id=None, bw_args=None) -> Page:
        cdp_url = self.get_cdp_url(user_id, platform_id, bw_args)
        browser = self.playwright_session.chromium.connect_over_cdp(cdp_url)
        page = browser.contexts[0].new_page()
        page: Page = page
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
