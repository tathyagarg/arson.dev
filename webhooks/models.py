from pydantic import BaseModel

class ListenerModel(BaseModel):
    name: str
    verification_type: int
    handler: str

    other_data: str = "" # Optional field for additional data

