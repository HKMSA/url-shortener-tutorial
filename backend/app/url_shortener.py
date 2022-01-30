# FIXME: return last insert id from db in insert()

from loguru import logger
import traceback
from utils.HashIds import Hashids
from db import Database
import urllib.request
from typing import Tuple, Dict
from utils.OutputHandler import std_content

class URLShortener:
  def __init__(self, db: Database=None, hostname:str=""):
    logger.debug("Initializing URLShortener class...")
    self.db = db
    self.hostname = hostname
  
  def clear_tables(self) -> None:
    """ Clear all tables in database
    
        For development purpose only, don't use in production
    """
    try:
      sql = "DELETE FROM url"
      sql2 = "DELETE FROM url_stats"
      self.db.execute(sql2)
      self.db.execute(sql)
    except Exception as e:
      logger.error(f"error: {e}")
      logger.error(traceback.format_exc())

  def insert(self, hashids:Hashids, ori:str) -> str:
    """ Insert original url and shortened url into database and returns generated hash
    
      Args:
        hashids (Hashids): hashids object
        ori (str): original url
      Returns:
        hash (str): generated hash
    """
    logger.info("-"*100)
    logger.info("insert() running...")
    hash = ""
    try:
      sql = "INSERT INTO url(shortened_url, original_url) VALUES (%s, %s)"
      args = ("", ori)
      rows = self.db.execute(sql, args)
      last_id = self.db.retrieve("SELECT LAST_INSERT_ID()")[0]["LAST_INSERT_ID()"]
      hash = hashids.encode(last_id)
      sql2 = "UPDATE url SET shortened_url=%s WHERE id=%s"
      args2 = (hash, last_id)
      rows2 = self.db.execute(sql2, args2)
      sql3 = "INSERT INTO url_stats(shortened_url, time_accessed, datetime_created) VALUES (%s, '', now())"
      rows3 = self.db.execute(sql3, hash)
      rows = rows and rows2 and rows3
    except Exception as e:
      logger.error(f"error: {e}")
      logger.error(traceback.format_exc())
    finally:
      return hash
  
  def retrieve(self, hash:str) -> str:
    """ Retrieve original URL by hash

      Args:
        hash (str): hash of the shortened URL
      Returns:
        result (str): string of the original URL
    """
    logger.info("-"*100)
    logger.info("retrieve() running...")
    result = ""
    try:
      sql = "SELECT original_url FROM url WHERE shortened_url=%s"
      res = self.db.retrieve(sql, hash)
      if res:
        result = res[0]["original_url"]
    except Exception as e:
      logger.error(f"error: {e}")
      logger.error(traceback.format_exc())
    finally:
      return result

  def validate_url(self, url:str) -> str:
    """ validate url

      Args:
        url (str): url to be validated
      Returns:
        url (str): un/edited url if valid, nothing if invalid
    """
    logger.info("-"*100)
    logger.info("validate_url() running...")
    valid_url = ""
    try:
      if url[0:7] != "http://" and url[0:8] != "https://":
        prefixes = ["http://", "http://www.", "https://", "https://www."]
        for prefix in prefixes:
          test_url = prefix + url
          if urllib.request.urlopen(test_url).getcode() == 200: # test url
            valid_url = test_url
            break
      else:
        if urllib.request.urlopen(url).getcode() == 200: # test original url
          valid_url = url
    except Exception as e:
      logger.error(f"error: {e}")
      logger.error(traceback.format_exc())
    finally:
      return valid_url

  def url_access(self, hash:str) -> None:
    """ Update time_accessed on url_stats table 
    
      Args:
        hash (str): hash of the shortened URL
    """
    logger.info("-"*100)
    logger.info("url_access() running...")
    new_res = ""
    try:
      sql_now = self.db.retrieve("SELECT now()")[0]["now()"]
      curr_date_time = sql_now.strftime("%d/%m/%Y %H:%M:%S")
      sql2 = "SELECT time_accessed FROM url_stats WHERE shortened_url=%s"
      res = self.db.retrieve(sql2, hash) # returned result is list of dict
      if not res[0]["time_accessed"]:
        new_res = curr_date_time
      else:
        new_res = res[0]["time_accessed"] + "@" + curr_date_time
      sql3 = "UPDATE url_stats SET time_accessed=%s WHERE shortened_url=%s"
      args3 = (new_res, hash)
      self.db.execute(sql3, args3)
    except Exception as e:
      logger.error(f"error: {e}")
      logger.error(traceback.format_exc())

  def find_matching_hash(self, url:str) -> str:
    """find matching hash value if original url exist

      Args:
        url (str): original url
      Returns:
        hash (str): matching hash value or nothing

    """
    logger.info("-"*100)
    logger.info("find_matching_hash() running...")
    hash = ""
    try:
      sql = "SELECT shortened_url FROM url WHERE original_url=%s"
      row = self.db.retrieve(sql, url)
      if row:
        hash = row[0]["shortened_url"]
    except Exception as e:
      logger.error(f"error: {e}")
      logger.error(traceback.format_exc())
    finally:
      return hash

  def shorten(self, args:dict, hashids:Hashids) -> Tuple[int,Dict[str,dict]]:
    """ Takes a long url and return the shortened url
  
      Args:
        args (dict): dictionary of arguments
        hashids (Hashids): hashids object
      Returns:
        status_code (int): status code of the response
        content (std_content): response object containing hash
    """
    logger.info("="*100)
    logger.info("shorten() running...")
    status_code = 500
    content = std_content()
    try:
      ori_url = args["url"].strip()
      if not ori_url: # do nothing if original link is blank
        status_code = 400
        content["message"] = "Original URL input is blank"
        content["data"] = {}
      elif self.validate_url(ori_url) == "":
        status_code = 400
        content["message"] = "Invalid URL"
        content["data"] = {}
      else:
        shortened_url_hash = self.find_matching_hash(ori_url)
        if not shortened_url_hash:
          status_code = 201
          shortened_url_hash = self.insert(hashids, ori_url)
        shorten_url = "http://" + self.hostname + "/" + shortened_url_hash #concatenate hash to host
        status_code = 200
        content["data"] = {"original_url": ori_url, "shortened_url": shorten_url}
    except Exception as e:
      logger.error(e)
      logger.error(traceback.format_exc())
    finally:
      return status_code, content
  
  def get_stats_by_hash(self, hash:str) -> Tuple[int,Dict[str,dict]]:
    """ Get stats of a url by hash
    
      Args:
        hash (str): hash of the shortened URL
      Returns:
        status_code (int): status code of the response
        content (std_content): response object containing stats
    """
    logger.info("="*100)
    logger.info("get_stats_by_hash() running...")
    status_code = 500
    content = std_content()
    try:
      sql = "SELECT url.shortened_url, url.original_url, url_stats.datetime_created, url_stats.time_accessed FROM url INNER JOIN url_stats ON url.shortened_url=url_stats.shortened_url WHERE url.shortened_url=%s"
      row = self.db.retrieve(sql, hash)
      if row:
        time_accessed = row[0]["time_accessed"].split("@")
        if not time_accessed[0]:
          num_click = 0
          time_accessed = []
        else:
          num_click = len(time_accessed)
        content["data"] = {
          "url": row[0]["original_url"],
          "shortened_url": "http://" + self.hostname + "/" + row[0]["shortened_url"],
          "datetime_created": row[0]["datetime_created"].strftime("%d/%m/%Y %H:%M:%S"),
          "number_of_clicks": num_click,
          "datetime_accessed": time_accessed
        }
        status_code = 200
      else:
        status_code = 404
        content["message"] = "No record found"
        content["data"] = {}
    except Exception as e:
      logger.error(f"error: {e}")
      logger.error(traceback.format_exc())
    finally:
      return status_code, content

  def get_stats_by_original_url(self, args:dict) -> Tuple[int,Dict[str,dict]]:
    """ return stats by original url
  
      Args:
        args (dict): dictionary of arguments
      Returns:
        status_code (int): status code of the response
        content (std_content): response object containing stats
    """
    logger.info("="*100)
    logger.info("get_stats_by_original_url() running...")
    status_code = 500
    content = std_content()
    try:
      ori_url = args["url"].strip()
      sql = "SELECT url.shortened_url, url.original_url, url_stats.datetime_created, url_stats.time_accessed FROM url INNER JOIN url_stats ON url.shortened_url=url_stats.shortened_url WHERE url.original_url=%s"
      row = self.db.retrieve(sql, ori_url)
      if row:
        time_accessed = row[0]["time_accessed"].split("@")
        if not time_accessed[0]:
          num_click = 0
          time_accessed = []
        else:
          num_click = len(time_accessed)
        content["data"] = {
          "url": row[0]["original_url"],
          "shortened_url": "http://" + self.hostname + "/" + row[0]["shortened_url"],
          "datetime_created": row[0]["datetime_created"].strftime("%d/%m/%Y %H:%M:%S"),
          "number_of_clicks": num_click,
          "datetime_accessed": time_accessed
          }
        status_code = 200
      else:
        status_code = 404
        content["message"] = "No record found"
        content["data"] = {}
    except Exception as e:
      logger.error(e)
      logger.error(traceback.format_exc())
    finally:
      return status_code, content

  def get_all(self) -> Tuple[int,Dict[str,list]]:
    ''' get basic info of all shortened urls
  
      Returns:
        status_code (int): status code of the response
        content (std_content): response object containing basic info
    '''
    logger.info('='*100)
    logger.info('get_all() running...')
    status_code = 500
    content = std_content("",[])
    try:
      sql = "SELECT url.shortened_url, url.original_url, url_stats.datetime_created FROM url INNER JOIN url_stats ON url.shortened_url=url_stats.shortened_url"
      rows = self.db.retrieve(sql)
      if not rows:
        status_code = 404
        content["message"] = "No record found"
        content["data"] = []
      else:
        for row in rows:
          short_url = "https://" + self.hostname + "/" + row["shortened_url"]
          content["data"].append({
            "url": row["original_url"],
            "shortened_url": short_url,
            "datetime_created": row["datetime_created"].strftime("%d/%m/%Y %H:%M:%S")
          })
        status_code = 200
    except Exception as e:
      logger.error(e)
      logger.error(traceback.format_exc())
    finally:
      return status_code, content

  def redirect(self, hash:str) -> str:
    """ Redirect to original URL

      Args:
        hash (str): hash of the shortened URL
      Returns:
        string of the original URL
    """
    logger.info("="*100)
    logger.info("redirect() running...")
    try:
      url = self.retrieve(hash)
      self.url_access(hash)
    except Exception as e:
      logger.error(e)
      logger.error(traceback.format_exc())
    finally:
      return self.validate_url(url)

# def main():
#   load_dotenv()
#   HOST = os.getenv("DB_HOST")
#   USER = os.getenv("DB_USER")
#   PASSWORD = os.getenv("DB_PASSWORD")
#   DATABASE = os.getenv("DB_DATABASE")

#   db = Database(HOST, USER, PASSWORD, DATABASE)
  
#   test = URLShortener()

#   # sql2 = "DROP TABLE url_stats"
#   # sql = "DROP TABLE url"
#   # sql2 = "CREATE TABLE url(id int(11) AUTO_INCREMENT UNIQUE, shortened_url varchar(7) CHARACTER SET utf8 COLLATE utf8_bin UNIQUE, original_url text(1000) NOT NULL, PRIMARY KEY(id, shortened_url));"
#   # sql = "CREATE TABLE url_stats(shortened_url varchar(7) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL UNIQUE PRIMARY KEY, time_accessed mediumtext, datetime_created datetime, FOREIGN KEY (shortened_url) REFERENCES url(shortened_url) ON DELETE CASCADE)"
  
#   # sql2 = "DESCRIBE url"
#   # sql = "DESCRIBE url_stats"

#   sql = "SELECT * FROM url_stats"
#   sql2 = "SELECT * FROM url"
#   # sql = "DELETE FROM url_stats"
#   # sql2 = "DELETE FROM url"

#   # sql = "SELECT LAST_INSERT_ID()"

#   # logger.debug(db.execute(sql2))
#   # logger.debug(db.execute(sql))
#   # logger.debug(db.retrieve(sql)[0]["datetime_created"].strftime("%d/%m/%Y %H:%M:%S"))
#   logger.debug(db.retrieve(sql))
#   logger.debug(db.retrieve(sql2))

#   # logger.debug(test.validate_url("www.google.com"))

# if __name__ == "__main__" :
#   main()