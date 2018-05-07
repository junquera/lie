from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from getpass import getpass

import time

driver = webdriver.Firefox()
driver.get('https://twitter.com')

# https://twitter.com/{{user}}/likes
LIMIT = 1000

def login_twitter(username, password):

    driver.get("https://twitter.com/login")

    username_field = driver.find_element_by_class_name("js-username-field")
    password_field = driver.find_element_by_class_name("js-password-field")

    username_field.send_keys(username)
    driver.implicitly_wait(1)

    password_field.send_keys(password)
    driver.implicitly_wait(1)

    driver.find_element_by_class_name("EdgeButtom--medium").click()


if __name__ == "__main__":
    username = input("user name : ")
    password = getpass("password  : ")

login_twitter(username, password)

username = input("Victim: ")
driver.get('https://twitter.com/' + username + '/likes')
html = driver.find_element_by_tag_name('html')
# html.text

body = driver.find_element_by_tag_name('body')
tl = []

def exists_css_element(element, parent):
    try:
        parent.find_element_by_css_selector(element)
        return True
    except:
        return False

tl = body.find_elements_by_css_selector('#timeline .stream ol > li')
last_len = len(tl)
last_len_eq = 0
while exists_css_element('.timeline-end.has-more-items', body) or last_len >= LIMIT:
# while len(body.find_elements_by_css_selector('#timeline .stream ol > li')) > len(tl):
    driver.execute_script(
        'arguments[0].scrollIntoView();', body.find_element_by_class_name('stream-footer'))
    # body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    tl = body.find_elements_by_css_selector('#timeline .stream ol > li')
    if len(tl) <= last_len:
        last_len_eq += 1
    else:
        last_len = len(tl)
        last_len_eq = 0

    if last_len_eq >= 3:
        break

found = {}
for t in tl:
    try:
        name = t.find_element_by_css_selector(
            '.content .stream-item-header .FullNameGroup .fullname').text
        user_name = t.find_element_by_css_selector(
            '.content .stream-item-header .username b').text
        # Con algunos elementos HTML dentro
        twit = t.find_element_by_css_selector(
            '.content .js-tweet-text-container').text
        verified = exists_css_element('.Icon.Icon--verified', t)

        if user_name in found:
            found[user_name]['count'] += 1
        else:
            found[user_name] = {'count': 1, 'verified': verified}

    except:
        pass

for x in found:
    print("@%s -%s-> %d likes" % (x, '(v)' if found[x]['verified'] else '', found[x]['count']))
