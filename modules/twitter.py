from os import getenv
from tweepy import OAuthHandler, API


class Twitter:
  def __init__(self):
    TWITTER_API_KEY = getenv('TWITTER_API_KEY')
    TWITTER_API_SECRET = getenv('TWITTER_API_SECRET')
    TWITTER_ACCESS_TOKEN = getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_SECRET = getenv('TWITTER_ACCESS_SECRET')

    twitter_auth = OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    twitter_auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    self.twitter = API(twitter_auth)

  def tweet(self, content):
    self.twitter.update_status(content)
