from pydantic import BaseModel

class ModelRes(BaseModel):
    error_status: bool = False
    error_type: str = ''
    error_name: str = ''
    error_reason: str = ''
