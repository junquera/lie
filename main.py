from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from getpass import getpass

import time

driver = webdriver.Firefox()
driver.get('https://twitter.com')

# https://twitter.com/{{user}}/likes
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
driver.get('https://twitter.com/eldiario/likes')
html = driver.find_element_by_tag_name('html')

for _ in range(10):
    body = browser.find_element_by_tag_name('body')
    time.sleep(2)

body.send_keys(Keys.PAGE_DOWN)
print(html)
