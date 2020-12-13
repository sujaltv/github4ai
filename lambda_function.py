import json
from datetime import datetime

from github4ai import bot_job

def lambda_handler(event, context):
  bot_job()
  return {
    'statusCode': 200,
    'body': f'Ran on {datetime.now().strftime("%a, %d %h %Y at %H:%M:%S")}.'
  }
