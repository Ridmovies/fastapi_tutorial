from fastapi import FastAPI

from app.web_router import router as web_router


app = FastAPI()

app.include_router(web_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}