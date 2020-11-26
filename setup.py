from os import path
from setuptools import setup, find_packages

requirements_txt = f'{path.dirname(path.realpath(__file__))}/requirements.txt'
with open(requirements_txt) as reqs:
  install_requires = reqs.read().splitlines()

setup(
  name='githubtopstar',
  version='0.0.1',
  author='TVS',
  packages=find_packages(exclude=['tests']),
  description='Tweet bot that tweets top-starred GitHub repository',
  long_description='''
    This is a bot that tweets every day the [top treding reporitory on
    GitHub](https://github.com/trending) that day.
  ''',
  python_requires='>=3.9',
  install_requires=install_requires
)