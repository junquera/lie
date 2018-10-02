import twitter
import secrets
# Library: https://github.com/bear/python-twitter
# Docs: https://python-twitter.readthedocs.io/en/latest/twitter.html?highlight=favorite
CONSUMER_KEY = secrets.CONSUMER_KEY
CONSUMER_SECRET = secrets.CONSUMER_SECRET
ACCESS_TOKEN_KEY = secrets.ACCESS_TOKEN_KEY
ACCESS_TOKEN_SECRET = secrets.ACCESS_TOKEN_SECRET

MAX_ITERATIONS = 30

user = input("Username > ")

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)

l = api.GetFavorites(screen_name=user)

count = 0
k = {}
while l and count < MAX_ITERATIONS:
    count += 1
    # Usually 20 twits per block
    block_s = 0
    try:
        for i in l:
            block_s += 1
            u = i.user

            if u.screen_name in k:
                k[u.screen_name] += 1
            else:
                k[u.screen_name] = 1

            # print("{} - {}".format(u.name, u.screen_name))
    except:
        pass

    print("[*] Block size: %d" % block_s)

    try:
        l = api.GetFavorites(screen_name=user, max_id=i.id)
    except:
        pass


print("[*] Total: %d" % len(k))

for n in k:
    print("{}\t{}".format(k[n], n))
