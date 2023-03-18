# Base FastAPI
from fastapi import FastAPI
# pydantic BaseModel
from pydantic import BaseModel
# Response types
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
# Cookies etc
from fastapi import Cookie
# Response
from fastapi import Response


app = FastAPI()


class Image(BaseModel):
    url: str
    name: str


class Base(BaseModel):
    name: str
    old: int
    etc: set[str] = []
    image: Image


@app.get("/test")
def api(ads_id: str | None = Cookie(default=None)) -> Response:
    return JSONResponse(content={"hi": ads_id})


@app.get("/", response_class=HTMLResponse)
def read_root():
    return f"""
            <html>
                <head>
                    <title>Rock paper scissor api</title>
                </head>
                <body>
                    <h1>Rock paper scissor api</h1>
                </body>
            </html>
            """


@app.get("/discord", response_class=RedirectResponse)
def read_root():
    return "https://discord.gg/v9D5VD4Rfp"

