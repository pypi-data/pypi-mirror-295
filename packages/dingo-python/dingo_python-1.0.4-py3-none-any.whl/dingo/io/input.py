from typing import Optional, List
from pydantic import BaseModel


class MetaData(BaseModel):
    """
    Metadata, output of converter.
    """
    data_id: str
    prompt: str = None
    content: str = None
    image: Optional[List] = None


class InputArgs(BaseModel):
    """
    Input arguments, input of project.
    """
    task_name: str = "dingo"
    eval_models: List[str] = ['default']
    input_path: str = "test/data/test_local_json.json"
    output_path: str = "test/outputs/"

    # Dataset setting
    data_format: str = "json"
    dataset: str = "hugging_face"
    datasource: str = ""

    # Huggingface specific setting
    huggingface_split: str = ""
    huggingface_config_name: Optional[str] = None

    # Spark params
    spark_master_url: str = ""
    spark_summary_save_path: str = ""

    # S3 param
    s3_ak: str = "PnLX8vRnWBeJ6xZs4TFh"
    s3_sk: str = "TByLSNsOZ6Fd4MEFeFA8wE1AkJbugzs8AQl0rDHl"
    s3_endpoint_url: str = "http://127.0.0.1:9000"
    s3_addressing_style: str = "auto"
    s3_bucket: str = "test"

    column_id: List[str] = []
    column_prompt: List[str] = []
    column_content: List[str] = []

    # Image param
    column_image: List[str] = []

    custom_config_path: Optional[str | dict] = None
