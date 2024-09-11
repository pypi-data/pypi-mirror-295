import re
import string
import jieba
import langid
import textstat
import wordninja

from typing import List, Tuple
from hanziconv import HanziConv
from nltk.tokenize import WordPunctTokenizer

from dingo.model.model import Model
from dingo.model.modelres import ModelRes
from dingo.model.rule.base import BaseRule
from dingo.model.rule.common.detect_lang import decide_language_by_str
from dingo.model.rule.common.util import (normalize, base_rps_frac_chars_in_dupe_ngrams, get_stop_words,
                                          split_paragraphs, TextSlice, Extractor, delete_punc_en, delete_punc_ch,
                                          get_tokens, is_sha256)
from dingo.config.config import DynamicRuleConfig
from dingo.io import MetaData


@Model.rule_register('QUALITY_INEFFECTIVENESS', ['text_base_all','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaOnlyUrl(BaseRule):
    """check whether content is only an url link."""
    custom_config = DynamicRuleConfig(pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        SEARCH_REGEX = re.compile(cls.custom_config.pattern)
        content_without_url = SEARCH_REGEX.sub("", input_data.content)
        if len(content_without_url.strip()) == 0:
            res.error_status = True
            res.error_type = 'QUALITY_INEFFECTIVENESS'
            res.error_name = cls.__name__
            res.error_reason = 'Content is only an url link.'
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', [''])
class QaChaosEnLine(BaseRule):
    """check whether content has english garbled characters at the line level."""
    custom_config = DynamicRuleConfig(file_path = '')

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content

        language = decide_language_by_str(content)
        if language != 'en':
            return res
        for content_line in content.split("\n"):
            af_en = delete_punc_en(content_line)
            af_ch = delete_punc_ch(af_en)
            str_len = len(af_ch)
            seg_len = len(list(jieba.cut(af_ch)))
            if seg_len == 0:
                continue
            if str_len / seg_len < 1.2:
                res.error_status = True
                res.error_type = 'QUALITY_INEFFECTIVENESS'
                res.error_name = cls.__name__
                res.error_reason = 'Content has english garbled characters in line: ' + content_line
                return res
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', [''])
class QaChaosZh(BaseRule):
    """check whether content has chinese garbled characters."""
    custom_config = DynamicRuleConfig(file_path = '', pattern = r'[a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]+(""|[\n\s])')

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content

        language = decide_language_by_str(content)
        if language != 'zh':
            return res
        af_en = delete_punc_en(content)
        af_ch = delete_punc_ch(af_en)
        text = re.sub(cls.custom_config.pattern, "", af_ch)
        simplified_text = HanziConv.toSimplified(text)
        seg_len = len(list(jieba.cut(simplified_text)))
        str_len = len(text)
        if str_len == 0 or seg_len == 0 and get_tokens(content, language) < 50:
            return res
        if str_len / seg_len > 1.2:
            return res
        else:
            res.error_status = True
            res.error_type = 'QUALITY_INEFFECTIVENESS'
            res.error_name = cls.__name__
            res.error_reason = 'Content has chinese garbled characters.'
            return res
        return res


@Model.rule_register('QUALITY_DISUNDERSTANDABILITY', ['text_base_all','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaEnterMore(BaseRule):
    """check whether content has 8 consecutive carriage returns."""
    custom_config = DynamicRuleConfig(key_list=[r"\n{8,}", r"\r\n{8,}"])

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        for p in cls.custom_config.key_list:
            SEARCH_REGEX = re.compile(p)
            match = SEARCH_REGEX.search(content)
            if match:
                res.error_status = True
                res.error_type = 'QUALITY_DISUNDERSTANDABILITY'
                res.error_name = cls.__name__
                res.error_reason = 'Content has 8 consecutive carriage returns.'
                return res
        return res


@Model.rule_register('QUALITY_DISUNDERSTANDABILITY', ['text_base_all','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaSpaceMore(BaseRule):
    """check whether content has 500 spaces."""
    custom_config = DynamicRuleConfig(pattern=" {500,}")

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        SEARCH_REGEX = re.compile(cls.custom_config.pattern)
        match = SEARCH_REGEX.search(content)
        if match:
            res.error_status = True
            res.error_type = 'QUALITY_DISUNDERSTANDABILITY'
            res.error_name = cls.__name__
            res.error_reason = 'Content has 500 spaces.'
            return res
        return res


@Model.rule_register('QUALITY_DISUNDERSTANDABILITY', ['text_base_all','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaEnterRatioMore(BaseRule):
    """check whether the number of enter / the number of content > 25%"""
    custom_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        if len(content) == 0:
            return res

        ratio = content.count("\n") / len(content)
        if ratio > 0.25:
            res.error_status = True
            res.error_type = 'QUALITY_DISUNDERSTANDABILITY'
            res.error_name = cls.__name__
            res.error_reason = 'The number of enter / the number of content > 25%.'
            return res
        return res


@Model.rule_register('QUALITY_DISFLUENCY', ['text_base_all','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaWordStuck(BaseRule):
    """check whether words are stuck."""
    custom_config = DynamicRuleConfig(
        key_list=[
            r"https?://[^\s]+|www.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            r"\.pdf$",
            r"\w+\.bat",
            r"(\/.*\/.*)",
            r"[01]+|[0-7]+|0x[0-9a-fA-F]+"
        ]
    )

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        language = decide_language_by_str(content)
        if language != 'en':
            return res

        for p in cls.custom_config.key_list:
            content = re.sub(p, "", content)
        word_list = [
            word.strip(string.punctuation) for word in
            re.split(r"[⁃>#%-.—,–!?;:\s|_/   =\\@\((.*?)\)\[(.*?)\]]\s*", content)
        ]
        for longest_string in word_list:
            if len(longest_string) > 45 and is_sha256(longest_string) == False:
                lan = decide_language_by_str(longest_string)
                cut = wordninja.split(longest_string)
                if lan == "en" and len(cut) > 1:
                    res.error_status = True
                    res.error_type = 'QUALITY_DISFLUENCY'
                    res.error_name = cls.__name__
                    res.error_reason = 'Words are stuck: ' + str(longest_string)
                    return res
        return res


@Model.rule_register('QUALITY_IRRELEVANCE', ['text_base_all','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaImgOrHtml(BaseRule):
    """check whether content has image links or html tags."""
    custom_config = DynamicRuleConfig(pattern=r"(<img[^>]*>)|<p[^>]*>(.*?)<\/p>|<o:p[^>]*>(.*?)<\/o:p>")

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content

        matches = re.findall(cls.custom_config.pattern, content)
        if matches:
            res.error_status = True
            res.error_type = 'QUALITY_IRRELEVANCE'
            res.error_name = cls.__name__
            res.error_reason = 'Content has image links or html tags: ' + ','.join(matches)
            return res
        return res


@Model.rule_register('QUALITY_IRRELEVANCE', ['text_base_all','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaInvisibleChar(BaseRule):
    """check whether content has invisible chars."""
    custom_config = DynamicRuleConfig(pattern=r"[\u2000-\u200F\u202F\u205F\u3000\uFEFF\u00A0\u2060-\u206F\uFEFF\xa0]")

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content

        matches = re.findall(cls.custom_config.pattern, content)
        if matches:
            res.error_status = True
            res.error_type = 'QUALITY_IRRELEVANCE'
            res.error_name = cls.__name__
            res.error_reason = 'Content has invisible chars: ' + ','.join(matches)
            return res
        return res