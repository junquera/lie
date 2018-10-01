import twitter
import secrets

CONSUMER_KEY = secrets.CONSUMER_KEY
CONSUMER_SECRET = secrets.CONSUMER_SECRET
ACCESS_TOKEN_KEY = secrets.ACCESS_TOKEN_KEY
ACCESS_TOKEN_SECRET = secrets.ACCESS_TOKEN_SECRET

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)

# GetSearch = RawQuery with https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-favorites-list
user = ''

l = api.GetFavorites(screen_name=user)

count = 0
k = {}
while l and count < 10:
    count += 1
    try:
        for i in l:
            u = i.user

            if u.screen_name in k:
                k[u.screen_name] += 1
            else:
                k[u.screen_name] = 1

            # print("{} - {}".format(u.name, u.screen_name))

        l = api.GetFavorites(screen_name=user, max_id=i.id)
    except:
        pass

print(k)
for n in k:
    print("{}\t{}".format(k[n], n))
