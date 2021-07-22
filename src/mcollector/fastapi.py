from fastapi import FastAPI

from mcollector.db import DBManager

app = FastAPI()


@app.on_event("startup")
async def startup_event() -> None:
    DBManager.start_mappers()
    await DBManager.recreate_db()


from mcollector.locations import views  # noqa
