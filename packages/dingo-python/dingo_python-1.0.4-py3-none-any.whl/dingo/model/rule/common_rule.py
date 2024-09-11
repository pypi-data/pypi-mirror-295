import re
import jieba
import langid
import textstat

from typing import List, Tuple
from hanziconv import HanziConv
from nltk.tokenize import WordPunctTokenizer, word_tokenize


from dingo.model.model import Model
from dingo.model.modelres import ModelRes
from dingo.model.rule.base import BaseRule
from dingo.model.rule.common.detect_lang import decide_language_by_str
from dingo.model.rule.common.util import (normalize, base_rps_frac_chars_in_dupe_ngrams, get_stop_words,
                                          split_paragraphs, TextSlice, Extractor)
from dingo.config.config import DynamicRuleConfig
from dingo.io import MetaData

@Model.rule_register('QUALITY_IRRELEVANCE', [])
class CommonPatternSearch(BaseRule):
    """let user input pattern to search"""
    custom_config = DynamicRuleConfig(pattern = "your pattern")

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        matches = re.findall(cls.custom_config.pattern, input_data.content)
        if matches:
            res.error_status = True
            res.error_type = 'QUALITY_IRRELEVANCE'
            res.error_name = cls.__name__
            res.error_reason = ','.join(list(set(matches)))
        return res


@Model.rule_register('QUALITY_INCOMPLETENESS', ['default','sft','pretrain','benchmark'])
class CommonColonEnd(BaseRule):
    """check whether the last char is ':'"""
    custom_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        if len(content) <= 0:
            return res
        if content[-1] == ':':
            res.error_status = True
            res.error_type = 'QUALITY_INCOMPLETENESS'
            res.error_name = cls.__name__
            res.error_reason = content[-100:]
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', ['default','sft','pretrain','benchmark','text_base_all','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class CommonContentNull(BaseRule):
    """check whether content is null"""
    custom_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        count = len(input_data.content.strip())
        if count == 0:
            res.error_status = True
            res.error_type = 'QUALITY_INEFFECTIVENESS'
            res.error_name = cls.__name__
            res.error_reason = 'Content is empty.'
        return res


@Model.rule_register('QUALITY_DISSIMILARITY', ['default','sft','pretrain','benchmark','text_base_all','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class CommonDocRepeat(BaseRule):
    """check whether content repeats"""
    custom_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        repeat_score = base_rps_frac_chars_in_dupe_ngrams(6, input_data.content)
        if repeat_score >= 80:
            res.error_status = True
            res.error_type = 'QUALITY_DISSIMILARITY'
            res.error_name = cls.__name__
            res.error_reason = 'Repeatability of text is too high, with ratio： ' + str(repeat_score)
        return res


@Model.rule_register('QUALITY_IRRELEVANCE', ['default','sft','pretrain','benchmark','text_base_all','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class CommonHtmlEntity(BaseRule):
    """check whether content has html entity"""
    custom_config = DynamicRuleConfig(key_list=[
        "nbsp",
        "lt",
        "gt",
        "amp",
        "quot",
        "apos",
        "hellip",
        "ndash",
        "mdash",
        "lsquo",
        "rsquo",
        "ldquo",
        "rdquo",
    ])

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content

        entities = cls.custom_config.key_list
        full_entities_1 = [f"&{entity}；" for entity in entities]
        full_entities_2 = [f"&{entity};" for entity in entities]
        full_entities_3 = [f"＆{entity};" for entity in entities]
        full_entities_4 = [f"＆{entity}；" for entity in entities]
        full_entities = full_entities_1 + full_entities_2 + full_entities_3 + full_entities_4
        # half_entity_1 = [f"{entity}；" for entity in entities]
        half_entity_2 = [f"＆{entity}" for entity in entities]
        half_entity_3 = [f"&{entity}" for entity in entities]
        # half_entity_4 = [f"{entity};" for entity in entities]
        half_entities = half_entity_2 + half_entity_3
        # maked_entities = [f"{entity}" for entity in entities]
        all_entities = full_entities + half_entities

        error_entity = []
        for entity in all_entities:
            if entity in content:
                res.error_status = True
                res.error_type = 'QUALITY_IRRELEVANCE'
                res.error_name = cls.__name__
                error_entity.append(entity)
        if len(error_entity) != 0:
            res.error_reason = ','.join(list(set(error_entity)))
        return res


@Model.rule_register('QUALITY_INSECURITY', ['default','sft','pretrain','benchmark'])
class CommonIDCard(BaseRule):
    """check if the content contains ID card. """
    custom_config = DynamicRuleConfig(pattern = r"(身\s{0,10}份|id\s{0,10}number\s{0,10}|identification|identity|\s{0,10}ID\s{0,10}No\s{0,10}|id\s{0,10}card\s{0,10}|NRIC\s{0,10}number\s{0,10}|IC\s{0,10}number\s{0,10}|resident\s{0,10}registration\s{0,10}|I.D.\s{0,10}Number\s{0,10})")

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        match = re.search(cls.custom_config.pattern, input_data.content, re.I)
        if match:
            person_id = Extractor().extract_id_card(input_data.content)
            if len(person_id) != 0:
                res.error_status = True
                res.error_type = 'QUALITY_INSECURITY'
                res.error_name = cls.__name__
                res.error_reason = str(person_id)
        return res


@Model.rule_register('QUALITY_DISFLUENCY', ['default','sft','pretrain','benchmark','text_base_all','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class CommonNoPunc(BaseRule):
    """check whether content has paragraph without punctuations"""
    custom_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        language = decide_language_by_str(content)
        if language != 'en':
            return res

        paragraphs = content.split('\n')
        longest_sentence = ''
        max_word_count = 0
        for paragraph in paragraphs:
            if len(paragraph.strip()) == 0:
                continue
            sentences = re.split("[-–.!?,;•/]", paragraph)
            for sentence in sentences:
                words = sentence.split()
                word_count = len(words)
                if word_count > max_word_count:
                    max_word_count = word_count
                    longest_sentence = sentence.strip()
        if int(max_word_count) > 56:
            res.error_status = True
            res.error_type = 'QUALITY_DISFLUENCY'
            res.error_name = cls.__name__
            res.error_reason = longest_sentence
        return res


@Model.rule_register('QUALITY_IRRELEVANCE', ['default','sft','pretrain','benchmark','text_base_all','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class CommonSpecialCharacter(BaseRule):
    """check whether content has special characters. """
    custom_config = DynamicRuleConfig(
        key_list=[
            r"u200e",
            # r"(\\\\;){3,}|(\{\}){3,}|(&nbsp;){3,}",
            r"&#247;|\? :",
            r"[�□]|\{\/U\}",
            r"U\+26[0-F][0-D]|U\+273[3-4]|U\+1F[3-6][0-4][0-F]|U\+1F6[8-F][0-F]"
        ]
    )

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content

        matches = []
        for p in cls.custom_config.key_list:
            m = re.findall(p, content)
            matches = matches + m
        if len(matches) != 0:
            res.error_status = True
            res.error_type = 'QUALITY_IRRELEVANCE'
            res.error_name = cls.__name__
            res.error_reason = str(list(set(matches)))
        return res


@Model.rule_register("QUALITY_IRRELEVANCE", [])
class CommonWatermark(BaseRule):
    """check whether content has watermarks."""
    custom_config = DynamicRuleConfig(key_list = [])

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        matches = re.findall('|'.join(cls.custom_config.key_list), input_data.content)
        if matches:
            res.error_status = True
            res.error_type = 'QUALITY_IRRELEVANCE'
            res.error_name = cls.__name__
            res.error_reason = ','.join(list(set(matches)))
        return res


@Model.rule_register("QUALITY_INCOMPLETENESS", ['pretrain'])
class CommonWordNumber(BaseRule):
    """check whether the number of word in [20, 100000] """
    custom_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        normalized_content = normalize(input_data.content)
        normalized_words = tuple(normalized_content.split())
        num_normalized_words = len(normalized_words)
        if num_normalized_words >= 20 and num_normalized_words < 100000:
            pass
        else:
            res.error_status = True
            res.error_type = 'QUALITY_INCOMPLETENESS'
            res.error_name = cls.__name__
            res.error_reason = "The number of word is: " + str(num_normalized_words)
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', ['pretrain'])
class CommonMeanWordLength(BaseRule):
    """check whether the mean length of word in [3, 10] """
    custom_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        normalized_content = normalize(input_data.content)
        normalized_words = tuple(normalized_content.split())
        num_normalized_words = len(normalized_words)
        if num_normalized_words == 0:
            return res

        num_chars = float(sum(map(len, normalized_words)))
        mean_length = num_chars / num_normalized_words
        mean_length = round(mean_length, 2)
        if mean_length >= 3 and mean_length < 10:
            pass
        else:
            res.error_status = True
            res.error_type = 'QUALITY_INEFFECTIVENESS'
            res.error_name = cls.__name__
            res.error_reason = "The mean length of word is: " + str(mean_length)
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', ['sft','pretrain','benchmark'])
class CommonSymbolWordRatio(BaseRule):
    """check whether the ratio of symbol / word is > 0.1"""
    custom_config = DynamicRuleConfig(key_list = ["#", "...", "…"])

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        raw_content = input_data.content
        raw_words = tuple(WordPunctTokenizer().tokenize(raw_content))
        num_raw_words = len(raw_words)
        if num_raw_words == 0:
            return res

        num_words = num_raw_words
        num_symbols = float(sum(
            raw_content.count(x) for x in cls.custom_config.key_list
        ))

        ratio = num_symbols / num_words
        if ratio > 0.4:
            res.error_status = True
            res.error_type = 'QUALITY_INEFFECTIVENESS'
            res.error_name = cls.__name__
            res.error_reason = "The ratio of symbol / word is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_INEFFECTIVENESS", ['pretrain'])
class CommonAlphaWords(BaseRule):
    """check whether the ratio of words that contain at least one alphabetic character > 0.6 """
    custom_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        language = decide_language_by_str(content)
        if language != 'en':
            return res
        words = word_tokenize(content)
        n_words = len(words)
        if n_words == 0:
            return res

        n_alpha_words = sum([any((c.isalpha() for c in w)) for w in words])
        ratio = n_alpha_words / n_words
        if ratio > 0.6:
            pass
        else:
            res.error_status = True
            res.error_type = 'QUALITY_INEFFECTIVENESS'
            res.error_name = cls.__name__
            res.error_reason = "The ratio of words that contain at least one alphabetic character is: " + str(ratio)
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', ['pretrain'])
class CommonStopWord(BaseRule):
    """check whether the ratio of stop word > 2"""
    custom_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        raw_content = input_data.content
        language = decide_language_by_str(raw_content)
        if language != 'en':
            return res
        raw_words = tuple(WordPunctTokenizer().tokenize(raw_content))
        num_raw_words = len(raw_words)
        if num_raw_words == 0:
            return res

        STOP_WORDS = get_stop_words("en")
        num_stop_words = sum(
            map(lambda w: w in STOP_WORDS, raw_words)
        )
        ratio = num_stop_words / num_raw_words
        if ratio < 0.06 or num_stop_words < 2:
            res.error_status = True
            res.error_type = 'QUALITY_INEFFECTIVENESS'
            res.error_name = cls.__name__
            res.error_reason = "The ratio of stop words is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_INCOMPLETENESS", ['pretrain'])
class CommonSentenceNumber(BaseRule):
    """check whether the number of sentence >= 3 """
    custom_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        raw_content = input_data.content

        SENT_PATTERN = re.compile(r'\b[^.!?]+[.!?]*', flags=re.UNICODE)
        num_sentence = len(SENT_PATTERN.findall(raw_content))
        if num_sentence < 3 or num_sentence > 7500:
            res.error_status = True
            res.error_type = 'QUALITY_INCOMPLETENESS'
            res.error_name = cls.__name__
            res.error_reason = "The number of sentence is: " + str(num_sentence)
        return res


@Model.rule_register("QUALITY_DISUNDERSTANDABILITY", [])
class CommonCurlyBracket(BaseRule):
    """check whether content contains curly bracket: { or } """
    custom_config = DynamicRuleConfig(pattern = "[{}]")

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        matches = re.findall(cls.custom_config.pattern, input_data.content)
        if matches:
            res.error_status = True
            res.error_type = 'QUALITY_DISUNDERSTANDABILITY'
            res.error_name = cls.__name__
            res.error_reason = ','.join(list(set(matches)))
        return res


@Model.rule_register("QUALITY_DISUNDERSTANDABILITY", ['pretrain'])
class CommonCapitalWords(BaseRule):
    """check whether capital words ratio > 0.3 """
    custom_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        raw_content = input_data.content
        raw_words = tuple(WordPunctTokenizer().tokenize(raw_content))
        num_raw_words = len(raw_words)
        if num_raw_words == 0:
            return res

        num_words = num_raw_words
        num_capital_words = sum([word.isupper() for word in raw_words])
        ratio = num_capital_words / num_words
        if ratio > 0.3 and ratio < 0.7:
            res.error_status = True
            res.error_type = 'QUALITY_DISUNDERSTANDABILITY'
            res.error_name = cls.__name__
            res.error_reason = "The ratio of capital words is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_INEFFECTIVENESS", ['sft','pretrain','benchmark'])
class CommonLoremIpsum(BaseRule):
    """check whether the ratio of lorem ipsum < 3e-08 """
    custom_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        normalized_content = normalize(input_data.content)
        num_normalized_content = len(normalized_content)
        if num_normalized_content == 0:
            return res

        SEARCH_REGEX = re.compile(r"lorem ipsum", re.IGNORECASE)
        num_occurrences = len(SEARCH_REGEX.findall(normalized_content))
        ratio = num_occurrences / num_normalized_content
        if ratio > 3e-08:
            res.error_status = True
            res.error_type = 'QUALITY_INEFFECTIVENESS'
            res.error_name = cls.__name__
            res.error_reason = "The ratio of lorem ipsum is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_DISUNDERSTANDABILITY", ['pretrain'])
class CommonUniqueWords(BaseRule):
    """check whether the ratio of unique words > 0.1"""
    custom_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        normalized_content = normalize(input_data.content)
        normalized_words = tuple(normalized_content.split())
        num_normalized_words = len(normalized_words)
        if num_normalized_words == 0:
            return res

        num_words = num_normalized_words
        num_unique_words = len(set(normalized_words))
        ratio = num_unique_words / num_words
        if ratio > 0.1:
            pass
        else:
            res.error_status = True
            res.error_type = 'QUALITY_DISUNDERSTANDABILITY'
            res.error_name = cls.__name__
            res.error_reason = "The ratio of unique words is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_INEFFECTIVENESS", ['pretrain'])
class CommonCharNumber(BaseRule):
    """check whether the number of char > 100 """
    custom_config = DynamicRuleConfig(threshold = 100)

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        text = input_data.content
        text = text.strip()
        text = text.replace(" ", "")
        text = text.replace("\n", "")
        text = text.replace("\t", "")
        num_char = len(text)
        if num_char < cls.custom_config.threshold:
            res.error_status = True
            res.error_type = 'QUALITY_INEFFECTIVENESS'
            res.error_name = cls.__name__
            res.error_reason = "The number of char is: " + str(num_char)
        return res


@Model.rule_register("QUALITY_DISUNDERSTANDABILITY", ['sft','pretrain','benchmark'])
class CommonLineStartWithBulletpoint(BaseRule):
    """check whether lines start with bullet points. """
    custom_config = DynamicRuleConfig(key_list = [
        "\u2022",  # bullet point
        "\u2023",  # triangular bullet point
        "\u25B6",  # black right pointing triangle
        "\u25C0",  # black left pointing triangle
        "\u25E6",  # white bullet point
        "\u25A0",  # black square
        "\u25A1",  # white square
        "\u25AA",  # black small square
        "\u25AB",  # white small square
        "\u2013",  # en dash
    ])

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        raw_content = input_data.content
        raw_lines: Tuple[TextSlice] = split_paragraphs(
            text=raw_content, normalizer=lambda x: x, remove_empty=True
        )
        num_lines = len(raw_lines)
        if num_lines == 0:
            return res

        num_occurrences = sum([line.text.lstrip().startswith(tuple(cls.custom_config.key_list)) for line in raw_lines])
        ratio = num_occurrences / num_lines
        if ratio > 0.9:
            res.error_status = True
            res.error_type = 'QUALITY_DISUNDERSTANDABILITY'
            res.error_name = cls.__name__
            res.error_reason = "The ratio of lines start with bulletpoint is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_INCOMPLETENESS", ['sft','pretrain','benchmark'])
class CommonLineEndWithEllipsis(BaseRule):
    """check whether lines end with ellipsis. """
    custom_config = DynamicRuleConfig(key_list = ["...", "…"])

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        raw_content = input_data.content
        raw_lines: Tuple[TextSlice] = split_paragraphs(
            text=raw_content, normalizer=lambda x: x, remove_empty=True
        )
        num_lines = len(raw_lines)
        if num_lines == 0:
            return res

        num_occurrences = sum([line.text.rstrip().endswith(tuple(cls.custom_config.key_list)) for line in raw_lines])
        ratio = num_occurrences / num_lines
        if ratio > 0.3:
            res.error_status = True
            res.error_type = 'QUALITY_INCOMPLETENESS'
            res.error_name = cls.__name__
            res.error_reason = "The ratio of lines end with ellipsis is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_INCOMPLETENESS", [])
class CommonLineEndWithTerminal(BaseRule):
    """check whether lines end with terminal punctuation mark. """
    custom_config = DynamicRuleConfig(key_list = [".", "!", "?", "”", "\""])

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        raw_content = input_data.content
        raw_lines: Tuple[TextSlice] = split_paragraphs(
            text=raw_content, normalizer=lambda x: x, remove_empty=True
        )
        num_lines = len(raw_lines)
        if num_lines == 0:
            return res

        terminal_marks = [line.text.rstrip()[-1] for line in raw_lines if line.text and line.text.rstrip()[-1] not in cls.custom_config.key_list]
        num_occurrences = sum([line.text.rstrip().endswith(tuple(cls.custom_config.key_list)) for line in raw_lines])
        ratio = num_occurrences / num_lines
        if ratio < 0.6:
            res.error_status = True
            res.error_type = 'QUALITY_INCOMPLETENESS'
            res.error_name = cls.__name__
            res.error_reason = ','.join(terminal_marks)
        return res


@Model.rule_register("QUALITY_INEFFECTIVENESS", ['sft','pretrain','benchmark'])
class CommonLineWithJavascript(BaseRule):
    """check whether line with the word Javascript. """
    custom_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        raw_content = input_data.content
        normalized_lines: Tuple[TextSlice] = split_paragraphs(
            text=raw_content, normalizer=normalize, remove_empty=True
        )
        num_lines = len(normalized_lines)
        if num_lines == 0:
            return res

        num_occurrences = sum(['javascript' in line.text for line in normalized_lines])
        num_not_occur = num_lines - num_occurrences
        if num_not_occur < 3 and num_lines > 3:
            res.error_status = True
            res.error_type = 'QUALITY_INEFFECTIVENESS'
            res.error_name = cls.__name__
            res.error_reason = "The lines with the word Javascript is: " + str(num_occurrences)
        return res


if __name__ == '__main__':
    content = """
    Exotica Volume II was the second album by Martin Denny, released in 1958.\n\nTrack listing\n\n \"Soshu Night Serenade\" (Ryōichi Hattori) – 2:08\n \"Island of Dreams\" (Laine, Denny) – 2:53\n \"Japanese Farewell Song (Sayonara)\" (Yoshda, Morgan) – 2:21\n \"Singing Bamboos\" (Madeline Lamb) – 2:07\n \"The Queen Chant (E Lili Ua E)\" (John Kaladana) – 2:46\n \"Wedding Song\" (Ke Kali Ne Au) (Charles E. King) – 2:44\n \"Escales\" (Jacques Ibert) – 2:39\n \"When First I Love\" (Denny) – 2:22\n \"August Bells\" (Gil Baumgart, Denny) – 2:14\n \"Bacoa\" (Les Baxter) – 1:59\n \"Ebb Tide\" (Robert Maxwell) – 3:11\n \"Rush Hour in Hong Kong\" (Abram Chasins) – 1:58\n\nPersonnel \n Martin Denny – piano, celeste, arrangements\n Arthur Lyman – vibes, marimba, xylophone, percussion\n Augie Colon – bongos, congas, Latin effects, bird calls\n Bernard Miller – string bass\n Jack Shoop – alto flute, baritone saxophone\n Roy Harte – drums, percussion\n Gil Baumgart – arranger, percussion\n Si Waronker – producer\n Ted Keep – engineer\n Val Valentin – engineer (uncredited)\n Garrett-Howard – cover design\n Sandy Warner – cover model\n\nReferences\n\n1958 albums\nExotica albums\nMartin Denny albums\nLiberty Records albums\nAlbums produced by Simon Waronker\nAlbums arranged by Martin Denny
    """
    data = MetaData(
        data_id = '',
        prompt = '',
        content = content
    )
    tmp = CommonAlphaWords().eval(data)
    print(tmp)