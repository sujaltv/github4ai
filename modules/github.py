from os import getenv
from enum import Enum
from requests import get


class GitHub:
  def __init__(self):
    self.__GITHUB_REPOS__ = 'https://api.github.com/search/repositories'

    self.github_headers = {
      'Authorization': f'token {getenv("GITHUB_SECRET")}'
    }

  @staticmethod
  def dict_to_query(dict):
    """Given a dictionary of query parameters, this method return a string
    formatted from @dict according to GitHub search syntax
    (https://developer.github.com/v3/search/#constructing-a-search-query)

    Args:
        dict (dict): A dictionary of query parameters

    Returns:
        str: Query string
    """

    query = []
    for (key, value) in dict.items():
      if isinstance(value, list):
        if len(value) > 5:
          value = value[:5]
        query.append('+'.join(list(map(lambda v: key + ':' + str(v), value))))
      else:
        query.append(key + ':' + str(value))
    return ' & '.join(query)

  def get_result(self, params):
    """Given search parameters, this method makes a network call to GitHub
    through the search API
    (https://developer.github.com/v3/search/#search-repositories) and returns
    the result

    Args:
        params (dict): A dictionary of search parameters

    Returns:
        [[dict]]: A list of repository details
    """
    response = get(
      self.__GITHUB_REPOS__,
      params=params,
      headers=self.github_headers
    ).json()

    if 'items' not in response or not len(response['items']):
      if 'message' in response:
        print(response['message'])
      return []
    return response['items']
