from loguru import logger
import traceback
import pymysql
from db import DBClass
import os
from dotenv import load_dotenv

class URLShortener:
  def __init__(self):
    self.db = DbClass()

  def __del__(self):
    pass

  def execute(self, query:str, args:list=[]) -> int:
    """Execute a sql query
    
    """
    logger.info(f'execute() running...')
    try:
      con = pymysql.connect(host=os.getenv('HOST'),user=os.getenv('USER'), password=os.getenv('PASSWORD'), database=os.getenv('DATABASE'))

      with con.cursor() as cur:
        rows = cur.execute(query, args=args)
        con.commit()
    except Exception as e:
      logger.error(e)
      logger.error(traceback.format_exc())
      con.rollback()
    finally:
      return rows

  def insert_value(self, shortened_url:str, original_url:str):
    query = f"INSERT INTO url(shortened_url,original_url) VALUES (%s,%s)"
    args = [shortened_url,original_url]
    # bad_query = f"INSERT INTO url(shortened_url,original_url) VALUES ({shortened_url},{original_url})" sql injection possible
    rows = self.execute(query,args)


if __name__ == '__main__':
  load_dotenv()
  urls = URLShortener()
  urls.insert_value('1234567','www.google.com')