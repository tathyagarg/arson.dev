from pydantic import BaseModel

class ListenerModel(BaseModel):
    name: str
    verification_type: int

    other_data: str = "" # Optional field for additional data

