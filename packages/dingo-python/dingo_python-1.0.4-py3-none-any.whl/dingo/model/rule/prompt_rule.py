from typing import List
import langid

from dingo.model import Model
from dingo.model.modelres import ModelRes
from dingo.model.rule.base import BaseRule
from dingo.io import MetaData


@Model.rule_register("QUALITY_INEFFECTIVENESS", [])
class PromptChineseProduceEnglish(BaseRule):
    """check whether chinese prompt produce english prediction"""
    rule_type = 'prompt'

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        lan_prompt = langid.classify(input_data.prompt)[0]
        lan_prediction = langid.classify(input_data.content)[0]
        if lan_prompt == 'zh' and lan_prediction == 'en':
            res.error_status = True
            res.error_type = 'QUALITY_INEFFECTIVENESS'
            res.error_name = cls.__name__
            res.error_reason = 'Chinese prompt, generate English content.'
        return res


@Model.rule_register("QUALITY_INEFFECTIVENESS", [])
class PromptEnglishProduceChinese(BaseRule):
    """check whether english prompt produce chinese prediction"""
    rule_type = 'prompt'

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        assert len(input_data) == 2
        lan_prompt = langid.classify(input_data.prompt)[0]
        lan_prediction = langid.classify(input_data.content)[0]
        if lan_prompt == 'en' and lan_prediction == 'zh':
            res.error_status = True
            res.error_type = 'QUALITY_INEFFECTIVENESS'
            res.error_name = cls.__name__
            res.error_reason = 'English prompt, generate Chinese content'
        return res
