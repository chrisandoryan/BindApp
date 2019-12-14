from flask import request, render_template, Response
from selenium.webdriver import Chrome, ChromeOptions
from app import app

import time

FLAG = "SG9ob2hvLiBIYXBweSBIb2xpZGF5Lg=="

def build_chrome_options():
    chrome_options = ChromeOptions()
    chrome_options.accept_untrusted_certs = True
    chrome_options.assume_untrusted_cert_issuer = True
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-impl-side-painting")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-seccomp-filter-sandbox")
    chrome_options.add_argument("--disable-breakpad")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--disable-cast")
    chrome_options.add_argument("--disable-cast-streaming-hw-encoding")
    chrome_options.add_argument("--disable-cloud-import")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-session-crashed-bubble")
    chrome_options.add_argument("--disable-ipv6")
    chrome_options.add_argument("--allow-http-screen-capture")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("disable-infobars"); # disabling infobars
    chrome_options.add_argument("--disable-extensions"); # disabling extensions
    chrome_options.add_argument("--disable-gpu"); # applicable to windows os only
    chrome_options.add_argument("--disable-dev-shm-usage"); # overcome limited resource problems
    return chrome_options


def valid_target(url):
    # TODO: add docker ip here
    for ban in ["localhost", "127.0.0.1", "::1", "0.0.0.0"]:
        if ban in url:
            return False
    return True


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Bye..')


@app.route('/snapshot', methods=['POST'])
def request_snapshot():
    url = request.form.get('url', "https://petircysec.com/")
    timeout = request.form.get('timeout', 1)

    if not valid_target(url):
        return 400, FLAG

    try:
        timeout = int(timeout)
    except Exception as e:
        timeout = 3

    time.sleep(timeout)

    driver = Chrome(build_chrome_options())
    driver.set_window_position(0, 0)
    # driver.set_window_size(800, 600)

    driver.set_page_load_timeout(20)
    driver.implicitly_wait(20)
    driver.get(url)

    # driver.set_window_size(800, 600)

    # sanity check
    if timeout < 0: timeout = 3
    time.sleep(timeout)

    png = driver.get_screenshot_as_base64()
    driver.quit()

    return Response(png, mimetype='application/base64')
