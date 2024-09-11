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


@Model.llm_register('openai')
class Openai(BaseLLM):
    client = None

    custom_config = DynamicLLMConfig(prompt_id="CONTEXT_RELEVANCE_PROMPT")

    @classmethod
    def create_client(cls):
        cls.client = OpenAI(api_key=cls.custom_config.key, base_url=cls.custom_config.api_url)

    @classmethod
    def call_api(cls, input_data: MetaData) -> ModelRes:
        if cls.client is None:
            cls.create_client()
        messages = [
            # {"role": "system",
            # "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
            # {"role": "user", "content": "你好，我叫李雷，1+1等于多少？"},
            {"role": "user", "content": get_prompt(cls.custom_config) + input_data.content}
        ]

        attempts = 0
        except_msg = ''
        while attempts < 3:
            try:
                completion = cls.client.chat.completions.create(
                    model=cls.custom_config.path,
                    messages=messages,
                    temperature=0.3,
                )
                response = str(completion.choices[0].message.content)
                log.info(response)

                if 'gpt' in cls.custom_config.path:
                    if response.startswith('```json'):
                        response = response[7:]
                    if response.endswith('```'):
                        response = response[:-3]
                res_json = json.loads(response)

                return ModelRes(
                    error_status=False if res_json['score'] == 1 else True,
                    error_type='QUALITY_IRRELEVANCE',
                    error_name=res_json['type'],
                    error_reason=response
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

