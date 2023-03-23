from typing import Annotated

import uvicorn
from fastapi import FastAPI, Query, Depends
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session

from db import models
from db.database import SessionLocal, engine
from redirect import router
from values import *

app = FastAPI(title="Rock-Paper-Scissor-API",
              description=api_description,
              version="0.0.1",
              contact=api_contact,
              license_info=api_license_info,
              openapi_tags=tags_metadata,
              debug=True)
app.include_router(router,
                   prefix="/redirect")
models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# noinspection PyTypeChecker
@app.get("/{code}/",
         tags=["api"],
         summary="API",
         description="the api website with post",
         response_description="api")
async def api(code: int, action: Annotated[str | None, Query(min_length=1, max_length=25)],
              db: Session = Depends(get_db)):
    if action == "create":
        code_open = db.query(models.Games).filter(models.Games.game_code == code).first()
        if code_open is not None:
            return {"used": code}
        db_game = models.Games(game_code=code, player1_win=0, player2_win=0, last_winner=-1)
        db.add(db_game)
        db.commit()
        db.refresh(db_game)
    if action == "join":
        code_open = db.query(models.Games).filter(models.Games.game_code == code).first()
        if code_open is None:
            return {"unused": code}

    return {"action": "b"}


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
