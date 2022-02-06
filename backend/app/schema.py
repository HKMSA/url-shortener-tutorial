from pydantic import BaseModel
from fastapi import Query
from typing import List

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

class StandardResponse(BaseModel):
  message: str = Query(None, title="Message to return")

class ShortenResponseData(BaseModel):
  original_url: str = Query(..., title="Original URL")
  shortened_url: str = Query(..., title="Shortened URL")

class StatsResponseData(BaseModel):
  url: str = Query(..., title="Original URL")
  shortened_url: str = Query(..., title="Shortened URL")
  datetime_created: str = Query(..., title="URL created datetime")

class DetailStatsResponseData(BaseModel):
  url: str = Query(..., title="Original URL")
  shortened_url: str = Query(..., title="Shortened URL")
  datetime_created: str = Query(..., title="URL created datetime")
  number_of_clicks: int = Query(..., title="Number of access to URL")
  datetime_accessed: List[str] = Query(..., title="List of URL accessed datetime")

class Schema:

  class ShortenRequest(BaseModel):
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

  class ShortenResponse(StandardResponse):
    data: ShortenResponseData = Query(None)

  class StatsResponse(StandardResponse):
    data: List[StatsResponseData] = Query(None)
  
  class StatsByHashResponse(StandardResponse):
    data: DetailStatsResponseData = Query(None)

  class StatsByOriginalUrlRequest(BaseModel):
    url: str = Query(..., title="Input URL you wanted to get stats", max_length=1000)

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
  
  class StatsByOriginalUrlResponse(StandardResponse):
    data: DetailStatsResponseData = Query(None)