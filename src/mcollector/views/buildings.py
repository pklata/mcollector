from typing import Any, Dict

from mcollector.app import app


@app.get("/buildings")
async def get_buildings() -> Dict[Any, Any]:
    return {"message": "Hello World"}
