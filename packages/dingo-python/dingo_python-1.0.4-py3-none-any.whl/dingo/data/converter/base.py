from functools import wraps
from typing import List, Protocol, Callable, Union, Dict
import json

from dingo.io import MetaData, InputArgs
from PIL import Image


class ConverterProto(Protocol):
    @classmethod
    def convertor(cls, input_args: InputArgs) -> Callable:
        ...


class BaseConverter(ConverterProto):
    converters = {}

    def __init__(self):
        pass

    @classmethod
    def convertor(cls, input_args: InputArgs) -> Callable:
        raise NotImplementedError()

    @classmethod
    def register(cls, type_name: str):
        def decorator(root_class):
            cls.converters[type_name] = root_class

            @wraps(root_class)
            def wrapped_function(*args, **kwargs):
                return root_class(*args, **kwargs)

            return wrapped_function

        return decorator

    @classmethod
    def find_levels_data(cls, data: json, levels: List[str]):
        res = data
        for key in levels:
            res = res[key]
        return res

    @classmethod
    def find_levels_image(cls, data: json, levels: List[str]) -> List:
        res = data
        for key in levels:
            res = res[key]
        if isinstance(res, List):
            return res
        return [res]


@BaseConverter.register('json')
class JsonConverter(BaseConverter):
    """
    Json file converter.
    """

    def __init__(self):
        super().__init__()

    @classmethod
    def convertor(cls, input_args: InputArgs) -> Callable:
        def _convert(raw: Union[str, Dict]):
            j = raw
            if isinstance(raw, str):
                j = json.loads(raw)
            for k, v in j.items():
                yield MetaData(**{
                    'data_id': cls.find_levels_data(v, input_args.column_id) if input_args.column_id != [] else str(k),
                    'prompt': cls.find_levels_data(v, input_args.column_prompt) if input_args.column_prompt != [] else '',
                    'content': cls.find_levels_data(v, input_args.column_content)
                })

        return _convert


@BaseConverter.register('plaintext')
class PlainConverter(BaseConverter):
    """
    Plain text file converter
    """
    data_id = 0

    def __init__(self):
        super().__init__()

    @classmethod
    def convertor(cls, input_args: InputArgs) -> Callable:
        def _convert(raw: Union[str, Dict]):
            if isinstance(raw, Dict):
                raw = json.dumps(raw)
            data = MetaData(**{
                'data_id': str(cls.data_id),
                'prompt': '',
                'content': raw
            })
            cls.data_id += 1
            return data

        return _convert


@BaseConverter.register('jsonl')
class JsonLineConverter(BaseConverter):
    """
    Json line file converter.
    """
    data_id = 0

    def __init__(self):
        super().__init__()

    @classmethod
    def convertor(cls, input_args: InputArgs) -> Callable:
        def _convert(raw: Union[str, Dict]):
            j = raw
            if isinstance(raw, str):
                j = json.loads(raw)
            cls.data_id += 1
            return MetaData(**{
                'data_id': cls.find_levels_data(j, input_args.column_id) if input_args.column_id != [] else str(
                    cls.data_id),
                'prompt': cls.find_levels_data(j, input_args.column_prompt) if input_args.column_prompt != [] else '',
                'content': cls.find_levels_data(j, input_args.column_content)
            })

        return _convert


@BaseConverter.register('listjson')
class ListJsonConverter(BaseConverter):
    """
    List json file converter.
    """

    data_id = 0

    def __init__(self):
        super().__init__()

    @classmethod
    def convertor(cls, input_args: InputArgs) -> Callable:
        def _convert(raw: Union[str, Dict]):
            l_j = raw
            if isinstance(raw, str):
                l_j = json.loads(raw)
            for j in l_j:
                yield MetaData(**{
                    'data_id': cls.find_levels_data(j, input_args.column_id) if input_args.column_id != [] else str(
                        cls.data_id),
                    'prompt': cls.find_levels_data(j, input_args.column_prompt) if input_args.column_prompt != [] else '',
                    'content': cls.find_levels_data(j, input_args.column_content)
                })
                cls.data_id += 1

        return _convert


@BaseConverter.register('hf-image')
class ImageConverter(BaseConverter):
    """
    Image converter.
    """

    data_id = 0

    def __init__(self):
        super().__init__()

    @classmethod
    def convertor(cls, input_args: InputArgs) -> Callable:
        def _convert(raw: Union[str, Dict]):
            j = raw
            if isinstance(raw, str):
                j = json.loads(raw)
            cls.data_id += 1
            return MetaData(**{
                'data_id': cls.find_levels_data(j, input_args.column_id) if input_args.column_id != [] else str(
                    cls.data_id),
                'image': cls.find_levels_image(j, input_args.column_image)
                if input_args.column_image != [] else [],
                'prompt': cls.find_levels_data(j, input_args.column_prompt) if input_args.column_prompt != [] else '',
                'content': cls.find_levels_data(j, input_args.column_content) if input_args.column_content != [] else ''
            })

        return _convert
