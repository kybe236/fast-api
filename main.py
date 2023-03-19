from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
from enum import Enum


app = FastAPI()


class Tags(Enum):
    user = "user",
    api = "api",
    redirect = "redirect",
    style = "style"


@app.post("/test/{arg}",
          response_class=JSONResponse,
          tags=[Tags.api],
          summary="API",
          description="the api website with post",
          response_description="api")
async def api(arg):
    return {"arg1": arg}


@app.get("/",
         response_class=HTMLResponse,
         tags=[Tags.user],
         summary="user main page",
         description="the user page with get",
         response_description="HTML main page")
def read_root():
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
def discord():
    return "https://discord.gg/v9D5VD4Rfp"


@app.get("/youtube",
         response_class=RedirectResponse,
         tags=[Tags.user, Tags.redirect],
         summary="redirect to youtube",
         description="redirect to the youtube channel",
         response_description="youtube URL redirect")
def youtube():
    return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


@app.get("/favicon.ico",
         response_class=FileResponse,
         tags=[Tags.style],
         summary="the favicon",
         description="the favicon for the page",
         response_description="favicon")
def favicon():
    return FileResponse("favicon")
