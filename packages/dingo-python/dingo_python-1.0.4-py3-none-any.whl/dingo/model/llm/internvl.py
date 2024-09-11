import json
import time

from dingo.model import Model
from dingo.model.llm.prompts.manager import get_prompt
from dingo.model.modelres import ModelRes
from dingo.io import MetaData
from dingo.model.llm.base import BaseLLM
from dingo.config.config import DynamicLLMConfig
from dingo.utils import log

try:
    from openai import OpenAI
except ImportError as e:
    log.warning("=========== openai register fail. Please check whether install OpenAI. ===========")


@Model.llm_register('internvl')
class InternVL(BaseLLM):
    client = None

    custom_config = DynamicLLMConfig(
        prompt_id="IMAGE_RELEVANCE_PROMPT"
    )

    @classmethod
    def create_client(cls):
        cls.client = OpenAI(api_key=cls.custom_config.key, base_url=cls.custom_config.api_url)

    @classmethod
    def call_api(cls, input_data: MetaData) -> ModelRes:
        if cls.client is None:
            cls.create_client()
        messages = [
            {"role": "user",
             "content": [{'type': 'text', 'text': get_prompt(cls.custom_config)},
                         {'type': 'image_url', 'image_url': {'url': input_data.prompt}},
                         {'type': 'image_url', 'image_url': {'url': input_data.content}}]
             }
        ]

        attempts = 0
        except_msg = ''
        if cls.custom_config.path is None:
            model_name = cls.client.models.list().data[0].id
        else:
            model_name = cls.custom_config.path
        while attempts < 3:
            try:
                completion = cls.client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=0.3,
                )
                response = str(completion.choices[0].message.content)
                log.info(response)

                if response.startswith('```json'):
                    response = response[7:]
                if response.endswith('```'):
                    response = response[:-3]

                res_json = json.loads(response)
                return ModelRes(
                    error_status=False if res_json['score'] == 1 else True,
                    error_type='QUALITY_IRRELEVANCE',
                    error_name='UNQUALIFIED',
                    error_reason=res_json['reason']
                )
            except Exception as e:
                attempts += 1
                time.sleep(1)
                except_msg = str(e)

        return ModelRes(
            error_status=True,
            error_type='QUALITY_IRRELEVANCE',
            error_name="API_LOSS",
            error_reason=except_msg
        )
