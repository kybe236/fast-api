from fastapi import FastAPI, Query, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
from enum import Enum
from typing import Annotated

app = FastAPI()


class Tags(Enum):
    user = "user",
    api = "api",
    redirect = "redirect",
    style = "style"


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
async def read_root():
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


@app.get("/favicon.ico",
         response_class=FileResponse,
         tags=[Tags.style],
         summary="the favicon",
         description="the favicon for the page",
         response_description="favicon")
async def favicon():
    return FileResponse("favicon")
