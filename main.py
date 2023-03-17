from fastapi import FastAPI, Query


app = FastAPI()


@app.get("/")
def read_root(name: list[str] | None = Query(default=None, max_length=20, min_length=3)):
    return {"name": name}
