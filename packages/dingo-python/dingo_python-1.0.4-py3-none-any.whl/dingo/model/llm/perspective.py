import pprint
import time

from dingo.model import Model
from dingo.model.modelres import ModelRes
from dingo.io import MetaData
from dingo.model.llm.base import BaseLLM
from dingo.config.config import DynamicLLMConfig
from dingo.utils import log

try:
    from googleapiclient import discovery
except ImportError:
    log.warning("=========== perspective register fail. Please check whether install googleapiclient. ===========")


@Model.llm_register('perspective')
class Perspective(BaseLLM):
    client = None

    custom_config = DynamicLLMConfig(
        api_url = 'https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1'
    )

    @classmethod
    def create_client(cls):
        if cls.client is None:
            cls.client = discovery.build(
                "commentanalyzer",
                "v1alpha1",
                developerKey=cls.custom_config.key,
                discoveryServiceUrl=cls.custom_config.api_url,
                static_discovery=False,
            )

    @classmethod
    def call_api(cls, input_data: MetaData) -> ModelRes:
        cls.create_client()
        analyze_request = {
            'comment': {'text': input_data.content},
            'requestedAttributes': {
                'TOXICITY': {},
                'SEVERE_TOXICITY': {},
                'IDENTITY_ATTACK': {},
                'INSULT': {},
                'PROFANITY': {},
                'THREAT': {},
                # 'SEXUALLY_EXPLICIT': {},
                # 'FLIRTATION': {},
            }
        }

        attempts = 0
        except_msg = ''
        while attempts < 3:
            try:
                response = cls.client.comments().analyze(body=analyze_request).execute()

                result = ModelRes()
                is_good = True
                error_list = []
                for e in response['attributeScores']:
                    value = response['attributeScores'][e]['summaryScore']['value']
                    if value > 0.6:
                        is_good = False
                        error_list.append(e)
                if is_good is False:
                    result.error_status = True
                    result.error_type = 'QUALITY_IRRELEVANCE'
                    result.error_name = 'PERSPECTIVE'
                    result.error_reason = ",".join(error_list)
                return result
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