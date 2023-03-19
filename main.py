from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse


app = FastAPI()


class ErrorHandler(Exception):
    def __init__(self, name: str):
        self.name = name


# noinspection PyUnusedLocal
@app.exception_handler(ErrorHandler)
async def handler(request: Request, exc: ErrorHandler):
    return JSONResponse(
        status_code=404,
        content={"ups": f"an error"}
    )


@app.get("/test/{arg}")
async def api(arg):
    return {"arg1": arg}


@app.get("/", response_class=HTMLResponse)
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


@app.get("/discord", response_class=RedirectResponse)
def discord():
    return "https://discord.gg/v9D5VD4Rfp"


@app.get("/youtube", response_class=RedirectResponse)
def youtube():
    return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
