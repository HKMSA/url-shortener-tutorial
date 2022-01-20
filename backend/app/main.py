from fastapi import FastAPI


app = FastAPI(
  title = "your title",
  description="Shorten your URL"
)

@app.get("/")
def run():
  return {"message": "hasdfahsdkf"}