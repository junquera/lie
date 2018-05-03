from selenium import webdriver

browser = webdriver.Firefox()
browser.get('https://twitter.com')

# https://twitter.com/{{user}}/likes
def login_twitter(username, password):
    driver = webdriver.Firefox()
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
