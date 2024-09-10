from PlayDrissionPage import RemoteBrowserClient, ChromiumPagePlus

if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()

    rbc = RemoteBrowserClient()
    page = rbc.get_d_page()

    page.get('https://www.baidu.com')
    page.xhr_request('GET', 'https://www.baidu.com', {}, {})

    tab_id = page.browser.tab_ids[-1]
    page: ChromiumPagePlus = page.browser.page.get_tab(tab_id)
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
