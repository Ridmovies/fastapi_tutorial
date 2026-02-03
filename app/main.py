from fastapi import FastAPI

from app.api.dev_router import router as dev_router
from app.web_router import router as web_router


app = FastAPI()

app.include_router(web_router)
app.include_router(dev_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}