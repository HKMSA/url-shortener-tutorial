import pymysql
from loguru import logger
import traceback
from dotenv import load_dotenv
import os

def test_connection():
  try:
    logger.info(f'running test_connection()')
    con = pymysql.connect(host=os.getenv('HOST'),user=os.getenv('USER'), password=os.getenv('PASSWORD'), database=os.getenv('DATABASE'))

    with con.cursor() as cur:
      cur.execute('SELECT VERSION()')
      version = cur.fetchone()
      logger.debug(f'Database version: {version[0]}')

  except Exception as e:
    logger.error(e)
    logger.error(traceback.format_exc())
  finally:
    con.close()

def execute(query:str) -> int:
  """Execute a sql query
  
  """
  logger.info(f'execute() running...')
  try:
    con = pymysql.connect(host=os.getenv('HOST'),user=os.getenv('USER'), password=os.getenv('PASSWORD'), database=os.getenv('DATABASE'))

    with con.cursor() as cur:
      rows = cur.execute(query)
      con.commit()
  except Exception as e:
    logger.error(e)
    logger.error(traceback.format_exc())
    con.rollback()
  finally:
    return rows


if __name__ == '__main__':
  load_dotenv()
  query = f'''
    CREATE TABLE url(
      id int AUTO_INCREMENT UNIQUE,
      shortened_url varchar(7) UNIQUE,
      original_url varchar(1000) NOT NULL,
      PRIMARY KEY(id, shortened_url)
    );
  '''
  execute(query)