#!/usr/bin/env python
import logging
import sqlalchemy.exc
import uvicorn
from fastapi import FastAPI, Query, Depends, Path, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated

from db import models
from db.database import engine, SessionLocal
from redirect import router
from values import *

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Rock-Paper-Scissor-API",
              description=api_description,
              version="0.0.1",
              contact=api_contact,
              license_info=api_license_info,
              openapi_tags=tags_metadata,
              debug=True)
app.include_router(router,
                   prefix="/redirect")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    logging.info("DB USED")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def match_win(player1, player2):
    logging.info("MATCHING WINNER")
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
        logging.info(f"GETTING LAST WINNER FROM {code}")
        try:
            game = db.query(models.Game).filter(models.Game.code == code).first()
            if game is not None:
                if game.next_picker == 1:
                    winner = match_win(game.player1, game.player2)
                    game.last_winner = winner
                    db.commit()
                    return {"last_winner": winner}
        except sqlalchemy.exc.IntegrityError as exception:
            logging.debug(exception)
            db.rollback()
            logging.info("SQL ERROR L=96")

    if action == "test":
        logging.info(f"TESTING IF USED {code}")
        game = db.query(models.Game).filter(models.Game.code == code).first()  # type: ignore[arg-type]

        if game is None:
            return {"unused": code}
        return {"used": code}

    if action == "create":
        logging.info(f"CREATE {code}")
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
            logging.debug("ROLLBACK L=110")
            raise HTTPException(status_code=409)
        return {"created": code}

    # play logic
    if action == "token":
        game = db.query(models.Game).filter(models.Game.code == code).first()  # type: ignore[arg-type]

        if game is None:
            logging.info("NOTHING IN DB")
            raise HTTPException(status_code=404)

        # if no token in db
        if game.token1 is None:
            logging.info("NO TOKEN1 IN DB")
            if token is not None:
                try:  # noqa
                    game.token1 = token
                    db.commit()
                    logging.info(f"LOGGING RANDOM TOKEN PLAYER 1 {code}: {token}")  # noqa for duplicated code
                except sqlalchemy.exc.IntegrityError as exception:
                    logging.debug(exception)
                    db.rollback()
                    logging.debug(f"LOGGING RANDOM TOKEN PLAYER 2 FAILED {code}: {token}")  # noqa for duplicated code
                    logging.info(f"DB SESSION CLOSED {code}: {token}")
                    return {"token1": "not set"}

        # if no token in db
        if game.token2 is None:
            logging.info("NO TOKEN2 ON DB")
            if token is not None:
                if token != game.token1:
                    logging.info("NOT SAME AS TOKEN1")
                    try:  # noqa
                        game.token2 = token
                        db.commit()
                        logging.info(f"LOGGING RANDOM TOKEN PLAYER 2 {code}: {token}")  # noqa for duplicated code
                    except sqlalchemy.exc.IntegrityError as exception:
                        logging.debug(exception)
                        db.rollback()
                        logging.debug(
                            f"LOGGING RANDOM TOKEN PLAYER 2 FAILED {code}: {token}")  # noqa for duplicated code
                        logging.info(f"DB SESSION CLOSED {code}: {token}")
                        return {"token1": "not set"}
                logging.info("SAME AS TOKEN")

    if action == "play":
        game = db.query(models.Game).filter(models.Game.code == code).first()

        if game is None:
            logging.debug("NO GAME OPEN")
            raise HTTPException(status_code=404)

        if token == game.token1:
            if game.next_picker == 1:
                if pick is None:
                    return {"specify_needed": "pick"}
                try:
                    game.player1 = pick
                    game.next_picker = 2
                    db.commit()
                    logging.info(f"PLAYER 1 PICKED {code}: {pick}")
                    return {"player2": pick}
                except sqlalchemy.exc.IntegrityError as exception:
                    logging.debug(exception)
                    db.rollback()
                    logging.debug("SQL PICK ERROR")
                    logging.info(f"DB SESSION CLOSED {code}: {token}")
                    return {"sql": "error"}

            return {"player2": "picking"}

        if token == game.token2:
            if game.next_picker == 2:
                if pick is None:
                    return {"specify_needed": "pick"}
                try:
                    game.player2 = pick
                    game.next_picker = 1
                    db.commit()
                    logging.info(f"PLAYER 2 PICKED {code}: {pick}")
                    return {"player1": pick}
                except sqlalchemy.exc.IntegrityError as exception:
                    logging.debug(exception)
                    db.rollback()
                    logging.debug("SQL PICK ERROR")
                    logging.info(f"DB SESSION CLOSED {code}: {token}")
                    return {"sql": "error"}

            return {"player1": "picking"}


@app.get("/",
         response_class=HTMLResponse,
         tags=["user"],
         summary="user main page",
         description="the user page with get",
         response_description="HTML main page")
async def read_root(request: Request):
    logging.info("/ VISITED")
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/favicon.ico",
         response_class=FileResponse,
         tags=["style"],
         summary="the favicon",
         description="the favicon for the page",
         response_description="favicon")
async def favicon():
    logging.info("FAVICON.ICO LOADED")
    return FileResponse("favicon")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, log_level="info")
