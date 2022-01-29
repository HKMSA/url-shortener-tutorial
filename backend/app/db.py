import pymysql
from loguru import logger
import traceback
import os
from dotenv import load_dotenv


class Database:
  def __init__(self, host:str, username:str, password:str, database:str):
    try:
      self.db = pymysql.connect(host=host, user=username, password=password, database=database)
      self.cur = self.db.cursor(pymysql.cursors.DictCursor)
      logger.debug("db connection initialized")
    except Exception as e:
      logger.error(e)
      logger.error(traceback.format_exc())

  def __del__(self):
    try:
      self.cur.close()
      self.db.close()
      logger.debug("db connection closed")
    except Exception as e:
      logger.error(e)
      logger.error(traceback.format_exc())

  def retrieve(self, sql:str, arg:list = []) -> dict: #return retrieved rows (type: tuple)
    result = {}
    try:
      # self.open_db()
      self.cur.execute(sql, arg)
      result = self.cur.fetchall()
    except Exception as e:
      logger.error(f'error: {e}')
      logger.error(traceback.format_exc())
      self.db.rollback()
    finally:
      # self.close_db()
      return result

  def execute(self, sql:str, arg:list = []) -> int: #return rows affected
    rows = 0
    try:
      # self.open_db()
      rows = self.cur.execute(sql, arg)
      self.db.commit()
    except Exception as e:
      logger.error(f'error: {e}')
      logger.error(traceback.format_exc())
      self.db.rollback()
    finally:
      # self.close_db()
      return rows

def main():
  load_dotenv()
  HOST = os.getenv('DB_HOST')
  USER = os.getenv('DB_USER')
  PASSWORD = os.getenv('DB_PASSWORD')
  DATABASE = os.getenv('DB_DATABASE')
  db = Database(HOST,USER,PASSWORD,DATABASE)
  sql = "SHOW TABLES"
  row = db.retrieve(sql)
  logger.debug(row)
if __name__ == "__main__" :
  main()