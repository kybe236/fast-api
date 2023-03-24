from typing import Annotated
from sqlalchemy.orm import Session

import uvicorn
from fastapi import FastAPI, Query, Depends, Path
from fastapi.responses import HTMLResponse, FileResponse
import sqlalchemy.exc

from redirect import router
from values import *

from db import models, database
from db.database import engine, SessionLocal


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


@app.get("/{code}/",
         tags=["api"],
         summary="API",
         description="the api website with post",
         response_description="api")
def api(code: Annotated[int, Path(le=111111111111111200)], action: Annotated[str | None, Query(max_length=20)],
        opt: int = None,
        db: Session = Depends(get_db)):
    if action == "test":
        game = db.query(models.Game).filter(models.Game.code == code).first()

        print(game)

        if game is None:
            return {"unused": code}
        return {"used": code}

    if action == "create":
        game = db.query(models.Game).filter(models.Game.code == code).first()

        if game is not None:
            return {"used": code}

        try:
            db_user = models.Game(code=code)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        except sqlalchemy.exc.IntegrityError as exception:
            db.rollback()
            return {"used": True, "exception": exception}
        return {"created": code}

    if action == "play":
        game = db.query(models.Game).filter(models.Game.code == code).first()

        if game is None:
            return {"unused": code}

        if game.token1 is None:
            try:
                game.token1 = opt
                db.commit()
            except sqlalchemy.exc.IntegrityError as exception:
                db.rollback()
                return {"token1": "not_set", "exception": exception}
        if game.token2 is None:
            try:
                game.token2 = opt
                db.commit()
            except sqlalchemy.exc.IntegrityError as exception:
                db.rollback()
                return {"token1": "not_set", "exception": exception}




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
