from twitter import *
import secrets
# Library: https://github.com/bear/python-twitter
# Docs: https://python-twitter.readthedocs.io/en/latest/twitter.html?highlight=favorite
CONSUMER_KEY = secrets.CONSUMER_KEY
CONSUMER_SECRET = secrets.CONSUMER_SECRET
ACCESS_TOKEN_KEY = secrets.ACCESS_TOKEN_KEY
ACCESS_TOKEN_SECRET = secrets.ACCESS_TOKEN_SECRET

MAX_ITERATIONS = 30

user = input("Username > ")

t = Twitter(
    auth=OAuth(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

l = t.favorites.list(screen_name=user)

count = 0
k = {}
while l and count < MAX_ITERATIONS:
    count += 1
    # Usually 20 twits per block
    block_s = 0
    try:
        for i in l:
            block_s += 1
            u = i.get('user')

            if u.get('screen_name') in k:
                k[u.get('screen_name')] += 1
            else:
                k[u.get('screen_name')] = 1

            # print("{} - {}".format(u.name, u.screen_name))
    except Exception as e:
        print(e)
        pass

    print("[*] Block size: %d" % block_s)

    try:
        l = t.favorites.list(screen_name=user, max_id=i.get('id'))
    except Exception as e:
        print(e)
        pass


print("[*] Total: %d" % len(k))

for n in k:
    print("{}\t{}".format(k[n], n))
