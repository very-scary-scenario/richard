import tweepy

from ayoade import get_line
from keys import (
    consumer_key, consumer_secret, access_token, access_token_secret,
)


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def tweet():
    api.update_status(get_line())


if __name__ == '__main__':
    tweet()
