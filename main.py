from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from getpass import getpass

import time

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()
driver.get('https://twitter.com')

import logging
logging.basicConfig(format='[*] %(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# https://twitter.com/{{user}}/likes
# TODO Contabilizar e ir sacando porcentajes
# TODO Configurar otro tipo de límites (por ejemplo antigüedad)
LIMIT = 500 # 3000

def add_css_rule(rule):

    driver.execute_script('''
    function addCss(cssString) {
    	var head = document.getElementsByTagName('head')[0];
      // return unless head;
      var newCss = document.createElement('style');
      newCss.type = "text/css";
      newCss.innerHTML = cssString;
      head.appendChild(newCss);
      console.log("Using ", newCss);
    }

    addCss('%s');
    ''' % rule)

def scroll_to(element):
    driver.execute_script("return arguments[0].scrollIntoView(true);", element)

def login_twitter(username, password):

    driver.get("https://twitter.com/login")

    username_field = driver.find_element_by_class_name("js-username-field")
    password_field = driver.find_element_by_class_name("js-password-field")

    username_field.send_keys(username)
    driver.implicitly_wait(1)

    password_field.send_keys(password)
    driver.implicitly_wait(1)

    driver.find_element_by_class_name("EdgeButtom--medium").click()

#
# if __name__ == "__main__":
#     username = input("user name : ")
#     password = getpass("password  : ")

username = 'leo.calero@protonmail.com'
password = 'L30.C4l3r0'
login_twitter(username, password)

# username = input("Victim: ")

username = 'sanchezcastejon'

driver.get('https://twitter.com/' + username + '/likes')
html = driver.find_element_by_tag_name('html')
# TODO Probar bs4 con html.text

body = driver.find_element_by_tag_name('body')
tl = []

def exists_css_element(element, parent):
    try:
        parent.find_element_by_css_selector(element)
        return True
    except:
        return False

tl = body.find_elements_by_css_selector('#timeline .stream > ol > li')
last_len = len(tl)
last_len_eq = 0

found = {}


def delete_element(element):
    t0 = time.time()
    driver.execute_script("""
    var element = arguments[0];
    element.parentNode.removeChild(element);
    """, element)
    # print("Deleted in %sseconds" % (time.time() - t0))

import re

# TODO Controlar "inianición"
# Times scrolled
c = 0
total = 0
# TODO Add signal to stop

add_css_rule("#timeline .stream ol > li { display: none; }")

all_likes = body.find_element_by_css_selector('.ProfileNav-list > li.ProfileNav-item.ProfileNav-item--favorites').text
all_likes = int(re.sub(r'[^0-9]', '', all_likes))

logging.warning("Extraction progress: %.02f%% (%d/%d)" % (100 * float(float(total)/float(all_likes)), total, all_likes))
while exists_css_element('.timeline-end.has-more-items', body) and total < LIMIT:
    driver.execute_script(
        'arguments[0].scrollIntoView();', body.find_element_by_class_name('stream-footer'))
    # body.send_keys(Keys.PAGE_DOWN)
    # time.sleep(1)

    for _ in range(50):
        body.send_keys(Keys.UP)
    # time.sleep(1)

    c += 1
    if c % 5 == 0:
        # time.sleep(1)

        tl = body.find_elements_by_css_selector('#timeline .stream ol > li')
        # TODO Medir tiempos y ver cuándo es mejor lanzar delete_element

        total = len(tl)
        logging.warning("Extraction progress: %.02f%% (%d/%d)" % (100 * float(float(total)/float(all_likes)), total, all_likes))

        for _ in range(50):
            body.send_keys(Keys.UP)

        for _ in range(50):
            body.send_keys(Keys.DOWN)

        for _ in range(50):
            body.send_keys(Keys.UP)

        # time.sleep(1)


def analyze_twit(t):
    # print("Time with the element: %ss" % (time.time() - t0))
    try:
        driver.execute_script("arguments[0].setAttribute('style','display: inherit!important;');",t)
        t0 = time.time()
        # En principio esta es la parte más lenta
        tc = t.find_element_by_css_selector('.content')
        # print("Time finding element content: %ss" % (time.time() - t0))

        t0 = time.time()
        name = tc.find_element_by_css_selector(
            '.stream-item-header .FullNameGroup .fullname').text
        # print(name)
        # print("Time finding name: %ss" % (time.time() - t0))
        t0 = time.time()
        user_name = tc.find_element_by_css_selector(
            '.stream-item-header .username b').text
        # print("Time finding user_name: %ss" % (time.time() - t0))
        t0 = time.time()
        # Con algunos elementos HTML dentro
        twit = tc.find_element_by_css_selector(
            '.js-tweet-text-container').text
        # print("Time finding twit: %ss" % (time.time() - t0))
        t0 = time.time()
        verified = exists_css_element('.Icon.Icon--verified', tc)
        # print("Time finding verified: %ss" % (time.time() - t0))

        if user_name in found:
            found[user_name]['count'] += 1
        else:
            found[user_name] = {'count': 1, 'verified': verified}
        # print("%s,%s" % (user_name, verified))

        delete_element(t)
    except Exception as e:
        # print(e)
        pass

    t0 = time.time()

tl = body.find_elements_by_css_selector('#timeline .stream ol > li')
'''
Hasta aquí llegamos rápido, podríamos probar a sacar todo el html y analizar con bs4
'''
for n in range(len(tl)):
    # print(tl[n].get_attribute('innerHTML'))
    logging.warning("Analysis progress: %.02f%% (%d/%d)" % (100 * float(n/float(all_likes)), n, all_likes))
    analyze_twit(tl[n])

# print("account,verified,likes")
with open('%s.csv' % username, 'w+') as f:
    for x in found:
        s = "%s,%s,%d" % (x, '(v)' if found[x]['verified'] else '', found[x]['count'])
        # print(s)
        f.write("%s\n" % s)
        f.flush()
