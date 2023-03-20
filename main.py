from fastapi import FastAPI, Query, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
from enum import Enum
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import hashlib

app = FastAPI()


class Tags(Enum):
    user = "user",
    api = "api",
    redirect = "redirect",
    style = "style"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token")
async def token_generate(form_dat: Annotated[OAuth2PasswordRequestForm, Depends()]):
    print(form_dat)
    return {"access_token": form_dat.password+form_dat.username, "token_type": "bearer"}


@app.post("/api",
          response_class=JSONResponse,
          tags=[Tags.api],
          summary="API",
          description="the api website with post",
          response_description="api")
async def api(name: Annotated[str, Query(max_length=20, min_length=2)]):
    return {"arg1": name}


@app.get("/",
         response_class=HTMLResponse,
         tags=[Tags.user],
         summary="user main page",
         description="the user page with get",
         response_description="HTML main page")
async def read_root(token: Annotated[str, Depends(oauth2_scheme)]):
    print(token)
    return f"""
            <html>
                <head>
                    <title>Rock paper scissor api</title>
                </head>
                <body>
                    <h1>Rock paper scissor api</h1>
                    <a href="/youtube">Youtube</a><br>
                    <a href="/discord">Discord</a>
                    
                </body>
            </html>
            """


@app.get("/discord",
         response_class=RedirectResponse,
         tags=[Tags.user, Tags.redirect],
         summary="redirect to discord",
         description="redirect to the rock-paper-scissor-api server",
         response_description="discord server invite URl redirect")
async def discord():
    return "https://discord.gg/v9D5VD4Rfp"


@app.get("/youtube",
         response_class=RedirectResponse,
         tags=[Tags.user, Tags.redirect],
         summary="redirect to youtube",
         description="redirect to the youtube channel",
         response_description="youtube URL redirect")
async def youtube():
    return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


@app.get("/favicon.ico",
         response_class=FileResponse,
         tags=[Tags.style],
         summary="the favicon",
         description="the favicon for the page",
         response_description="favicon")
async def favicon():
    return FileResponse("favicon")
