from typing import Annotated

import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse

from redirect import router
from values import *

app = FastAPI(title="Rock-Paper-Scissor-API",
              description=api_description,
              version="0.0.1",
              contact=api_contact,
              license_info=api_license_info,
              openapi_tags=tags_metadata)
app.include_router(router,
                   prefix="/redirect")


@app.post("/api",
          response_class=JSONResponse,
          tags=["api"],
          summary="API",
          description="the api website with post",
          response_description="api")
async def api(name: Annotated[str, Query(max_length=20, min_length=2)]):
    return {"arg1": name}


@app.get("/",
         response_class=HTMLResponse,
         tags=["user"],
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
                    <a href="/redirect/youtube">Youtube</a><br>
                    <a href="/redirect/discord">Discord</a>
                    
                </body>
            </html>
            """


@app.get("/favicon.ico",
         response_class=FileResponse,
         tags=["style"],
         summary="the favicon",
         description="the favicon for the page",
         response_description="favicon")
async def favicon():
    return FileResponse("favicon")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, log_level="info")
