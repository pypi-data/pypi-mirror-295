from typing import Protocol, List
from pydantic import BaseModel

from dingo.model.modelres import ModelRes
from dingo.io import MetaData


class BaseLLM(Protocol):
    @classmethod
    def call_api(cls, input_data: MetaData) -> ModelRes:
        ...
