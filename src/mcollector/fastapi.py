from fastapi import FastAPI

from mcollector.db import DBManager

app = FastAPI()


@app.on_event("startup")
async def startup_event() -> None:
    DBManager.start_mappers()
    await DBManager.create_db()


# Import views
# Import mappings
from mcollector.locations import mappings  # noqa
from mcollector.locations import views  # noqa
