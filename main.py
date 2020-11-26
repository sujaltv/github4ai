from dotenv import load_dotenv
load_dotenv()

import random
import time
from datetime import datetime
import schedule
from yaml import load, Loader

from modules.github import GitHub
from modules.twitter import Twitter

github = GitHub()
twitter = Twitter()


def get_tweet_content_from_res(gh_res):
  """From the response object returned by GitHub's API, this function buils the
  content to be tweeted

  Args:
      gh_res (dict): A dictionary of repository details

  Returns:
      str: The string to be tweeted.
  """
  tweet_content = gh_res["name"]
  if gh_res["language"]:
    tweet_content += f' in {gh_res["language"]}'
  tweet_content += f' by {gh_res["owner"]["login"]} ({gh_res["html_url"]}).'
  if gh_res["description"]:
    tweet_content += f'\n{gh_res["description"][:100]}'
    if (len(gh_res["description"])) > 100:
      tweet_content += '...'
  return tweet_content

with \
  open('./config/keywords.yml') as kwds,\
  open('./config/languages.yml') as lngs:
  # Add quotes are each array item to account for phrases
  keywords = list(map(lambda k: f'"{k}"', load(kwds, Loader=Loader)))
  languages = list(map(lambda k: f'"{k}"', load(lngs, Loader=Loader)))

def bot_job():
  random.seed(time.time())
  repos = []
  count = 0

  # If no repository found, retry with a different random search configuration
  while len(repos) == 0 and count < 10:
    repos_by_stars = {
      "q": GitHub.dict_to_query({
        f'{" OR ".join(random.choices(keywords, k=2))} in': 'readme',
        'language': random.choice(languages),
        'fork': 'true',
      "sort": "created"
      }),
      "page": 1,
      # "per_page": 1
    }

    repos = github.get_result(repos_by_stars)
    count += 1

  if len(repos) == 0:
    return

  tweet_content = get_tweet_content_from_res(random.choice(repos))
  twitter.tweet(tweet_content)
  print(f'Tweeter on {datetime.now().strftime("%a, %d %h %Y at %H:%M")}.')


if __name__ == '__main__':
  schedule.every().day.at("00:00").do(bot_job)
  schedule.every().day.at("12:00").do(bot_job)

  while True:
    print(f'Log on {datetime.now().strftime("%a, %d %h %Y at %H:%M")}.')
    schedule.run_pending()
    time.sleep(60)
