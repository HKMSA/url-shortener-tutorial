from pydantic import BaseModel
from fastapi import Query

class Tag:
  tags_metadata = [
    {
      "name": "URL",
      "description": "Includes function that shorten URL"
    },
    {
      "name": "Getting stats",
      "description": "Include functions that returns statistics of URLs"
    },
    {
      "name": "Redirect",
      "description": "Enter url hash to redirect"
    }
  ]

class Schema:

  class URLRequestSchema(BaseModel):
    url: str = Query(..., title="Input URL you wanted to shorten", max_length=1000)

    class Example:
      examples = {
        'example 1': {
          'summary': 'Google website',
          'description': 'Official website of Google',
          'value': {
            'url': 'https://www.google.com',
          }
        }
      }