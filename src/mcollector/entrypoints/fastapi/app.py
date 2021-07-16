from fastapi import FastAPI

app = FastAPI()

from mcollector.entrypoints.fastapi import views  # noqa
