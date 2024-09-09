from pydantic.main import BaseModel
from pydantic import ConfigDict


class Base(BaseModel):
    model_config = ConfigDict(frozen=True)
