class NotFoundError(Exception):
    def __init__(self, model_name: str, _id: int):
        self.message = f"{model_name} with id: {_id} not found."
