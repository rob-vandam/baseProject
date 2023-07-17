from typing import List, Union

from pydantic import BaseModel

class User(BaseModel):
    authtoken: str
    refreshtoken: str
    idtoken: str
    admin_id: int
    app_id: int
    action: str
    chain_id: int
    lang: str
    class Config:
        from_attributes = True


