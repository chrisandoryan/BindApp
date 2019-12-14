from flask import request, render_template, Response
from selenium.webdriver import Firefox
from app import app

import time

FLAG = "SG9ob2hvLiBIYXBweSBIb2xpZGF5Lg=="

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

    driver = Firefox()
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
