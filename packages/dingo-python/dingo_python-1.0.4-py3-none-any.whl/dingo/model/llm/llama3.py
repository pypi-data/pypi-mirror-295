import json
import time

from transformers import AutoTokenizer, AutoModelForCausalLM

from dingo.model import Model
from dingo.model.llm.prompts.manager import get_prompt
from dingo.model.modelres import ModelRes
from dingo.io import MetaData
from dingo.model.llm.base import BaseLLM
from dingo.config.config import DynamicLLMConfig
from dingo.utils import log

try:
    import torch
except ImportError as e:
    log.warning("=========== llama3 register fail. Please check whether install torch. ===========")


@Model.llm_register('llama3')
class LLaMa3(BaseLLM):
    model = None
    tokenizer = None

    custom_config = DynamicLLMConfig(prompt_id="CONTEXT_RELEVANCE_PROMPT")

    @classmethod
    def generate_words(cls, input_data: str) -> json:
        if cls.model is None:
            cls.model = AutoModelForCausalLM.from_pretrained(
                cls.custom_config.path,
                torch_dtype=torch.bfloat16,
                device_map="auto",
            )
        if cls.tokenizer is None:
            cls.tokenizer = AutoTokenizer.from_pretrained(cls.custom_config.path)

        messages = [
            {"role": "system", "content": input_data},
        ]

        input_ids = cls.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(cls.model.device)

        terminators = [
            cls.tokenizer.eos_token_id,
            cls.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]

        outputs = cls.model.generate(
            input_ids,
            max_new_tokens=256,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )
        response = outputs[0][input_ids.shape[-1]:]
        return json.loads(cls.tokenizer.decode(response, skip_special_tokens=True))

    @classmethod
    def call_api(cls, input_data: MetaData) -> ModelRes:
        attempts = 0
        except_msg = ''
        while attempts < 3:
            try:
                response = cls.generate_words(get_prompt(cls.custom_config) % input_data.content)

                return ModelRes(
                    error_status=False if response['score'] > 6 else True,
                    error_type='QUALITY_IRRELEVANCE',
                    error_name=response['type'],
                    error_reason=response['reason']
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
