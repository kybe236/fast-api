import logging
from typing import Annotated

import sqlalchemy.exc
import uvicorn
from fastapi import FastAPI, Query, Depends, Path, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session

from db import models
from db.database import engine, SessionLocal
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


def match_win(player1, player2):
    match player1:
        case 1:
            match player2:
                case 1:
                    return 0
                case 2:
                    return 2
                case 3:
                    return 1
        case 2:
            match player2:
                case 1:
                    return 0
                case 2:
                    return 2
                case 3:
                    return 1
        case 3:
            match player2:
                case 1:
                    return 0
                case 2:
                    return 2
                case 3:
                    return 1


@app.get("/{code}/",
         tags=["api"],
         summary="API",
         description="the api website with post",
         response_description="api")
def api(code: Annotated[int, Path(le=111111111111111200)], action: Annotated[str | None, Query(max_length=20)],
        token: int = None,
        pick: int = None,
        db: Session = Depends(get_db)):
    if action == "last_winner":
        try:
            game = db.query(models.Game).filter(models.Game.code == code).first()
            if game is not None:
                winner = match_win(game.player1, game.player2)
                return {"last_winner": winner}
        except sqlalchemy.exc.IntegrityError as exception:
            logging.debug(exception)
            db.rollback()

    if action == "test":
        game = db.query(models.Game).filter(models.Game.code == code).first()  # type: ignore[arg-type]

        if game is None:
            return {"unused": code}
        return {"used": code}

    if action == "create":
        game = db.query(models.Game).filter(models.Game.code == code).first()  # type: ignore[arg-type]

        if game is not None:
            return {"used": code}

        try:
            db_user = models.Game(code=code)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        except sqlalchemy.exc.IntegrityError as exception:
            logging.debug(exception)
            db.rollback()
            raise HTTPException(status_code=409)
        return {"created": code}

    # play logic
    if action == "play":
        game = db.query(models.Game).filter(models.Game.code == code).first()  # type: ignore[arg-type]

        if game is None:
            raise HTTPException(status_code=404)

        # if no token in db
        if game.token1 is None:
            if token is not None:
                try:
                    game.token1 = token
                    db.commit()
                except sqlalchemy.exc.IntegrityError as exception:
                    logging.debug(exception)
                    db.rollback()
                    return {"token1": "not_set"}
                finally:
                    db.close()

        # if no token in db
        if game.token2 is None:
            if token is not None:
                if token != game.token1:
                    try:
                        game.token2 = token
                        db.commit()
                    except sqlalchemy.exc.IntegrityError as exception:
                        logging.debug(exception)
                        db.rollback()
                        return {"token1": "not_set"}
                    finally:
                        db.close()

        if token == game.token1:
            if game.next_picker == 1:
                if pick is None:
                    return {"specify_needed": "pick"}
                try:
                    game.player1 = pick
                    game.next_picker = 2
                    db.commit()
                    return {"player2": pick}
                except sqlalchemy.exc.IntegrityError as exception:
                    logging.debug(exception)
                    db.rollback()
                    return {"sql": "error"}
                finally:
                    db.close()
            return {"player2": "picking"}

        if token == game.token2:
            if game.next_picker == 2:
                if pick is None:
                    return {"specify_needed": "pick"}
                try:
                    game.player2 = pick
                    game.next_picker = 1
                    db.commit()
                    return {"player1": pick}
                except sqlalchemy.exc.IntegrityError as exception:
                    logging.debug(exception)
                    db.rollback()
                    return {"sql": "error"}
                finally:
                    db.close()
            return {"player1": "picking"}


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
