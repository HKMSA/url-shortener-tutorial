# FIXME: handle bad request

from fastapi import Body, FastAPI, status
from fastapi.responses import RedirectResponse, JSONResponse
import os
from dotenv import load_dotenv
import uvicorn
from schema import Tag, Schema
from fastapi.middleware.cors import CORSMiddleware
from db import Database
from url_shortener import URLShortener
from utils.HashIds import Hashids

load_dotenv()

HOST = os.getenv('DB_HOST')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DB_DATABASE')
salt = "fjasdlfjalff"
allowed_alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
hostname = os.getenv("BACKEND_HOST")

tag = Tag()
schema = Schema()

app = FastAPI(
  title = "URL Shortener",
  description = "It accepts long URL and returns shorter URL",
  version = "0.0.2",
  openapi_tags=tag.tags_metadata
)

# allow CORS setting
origins = ['*']

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# security setting
# https://geekflare.com/http-header-implementation/https://geekflare.com/http-header-implementation/
HEADERS = {
  # CORS setting
  "Access-Control-Allow-Credentials": "true",
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "*",
  "Access-Control-Allow-Headers": "*",
  # security setting
  "X-Frame-Options": "SAMEORIGIN",
  "X-Content-Type-Options": "nosniff",
  "X-XSS-Protection": "1; mode=block",
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
  "Expect-CT": "max-age=86400, enforce", # enforcement of Certificate Transparency for 24 hours
  "Content-Security-Policy": "default-src https:"
}

hashids = Hashids(salt=salt, alphabet=allowed_alphabet, min_length=7)
db = Database(HOST, USER, PASSWORD, DATABASE)
url_short = URLShortener(db=db, hostname=hostname)

@app.get("/_healthcheck", status_code=status.HTTP_200_OK)
def healthcheck():
  content = {"status": "OK"}
  return JSONResponse(content=content, headers=HEADERS)

@app.post("/shorten", tags=["URL"], response_class=JSONResponse)
def shorten_url(request:schema.URLRequestSchema = Body(...,examples=schema.URLRequestSchema.Example.examples)) -> JSONResponse:
  args = request.dict()
  status_code, content = url_short.shorten(args, hashids)
  return JSONResponse(content=content, headers=HEADERS, status_code=status_code)

@app.get("/stats",tags=["Getting stats"], response_class=JSONResponse)
def get_all() -> JSONResponse:
  status_code, content = url_short.get_all()
  return JSONResponse(content=content, headers=HEADERS, status_code=status_code)

@app.get("/stats/{hash}",tags=["Getting stats"], response_class=JSONResponse)
def get_stats_by_hash(hash:str) -> JSONResponse:
  status_code, content = url_short.get_stats_by_hash(hash)
  return JSONResponse(content=content, headers=HEADERS, status_code=status_code)

@app.post("/stats/find",tags=["Getting stats"], response_class=JSONResponse)
def get_stats_by_original_url(request:schema.URLRequestSchema = Body(..., examples=schema.URLRequestSchema.Example.examples)) -> JSONResponse:
  args = request.dict()
  status_code, content = url_short.get_stats_by_original_url(args)
  return JSONResponse(content=content, headers=HEADERS, status_code=status_code)

@app.get("/{hash}", tags=["Redirect"], response_class=RedirectResponse)
def redirect(hash:str) -> RedirectResponse:
  return RedirectResponse(url_short.redirect(hash))


if __name__ == '__main__':
  uvicorn.run("main:app", host="localhost", port=8000, reload=True)