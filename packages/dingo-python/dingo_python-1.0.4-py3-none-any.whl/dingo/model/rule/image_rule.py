import numpy as np
from PIL import Image
from typing import List

from dingo.model.model import Model
from dingo.model.modelres import ModelRes
from dingo.model.rule.base import BaseRule
from dingo.config.config import DynamicRuleConfig
from dingo.io import MetaData

try:
    import torch
except ModuleNotFoundError as e:
    raise ModuleNotFoundError("You need to install `torch`, try `pip install torch`")
try:
    import pyiqa
except ModuleNotFoundError as e:
    raise ModuleNotFoundError("You need to install `pyiqa`, try `pip install pyiqa`")


@Model.rule_register('QUALITY_INEFFECTIVENESS', ['img'])
class ImageValid(BaseRule):
    """check whether image is not all white or black"""
    custom_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        if isinstance(input_data.image[0], str):
            img = Image.open(input_data.image[0])
        else:
            img = input_data.image[0]
        img_new = img.convert("RGB")
        img_np = np.asarray(img_new)
        if np.all(img_np == (255, 255, 255)) or np.all(img_np == (0, 0, 0)):
            res.error_status = True
            res.error_type = 'QUALITY_INEFFECTIVENESS'
            res.error_name = cls.__name__
            res.error_reason = 'Image is not valid: all white or black'
        img.close()
        img_new.close()
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', ['img'])
class ImageSizeValid(BaseRule):
    """check whether image ratio of width to height is valid"""
    custom_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        if isinstance(input_data.image[0], str):
            img = Image.open(input_data.image[0])
        else:
            img = input_data.image[0]
        width, height = img.size
        aspect_ratio = width / height
        if aspect_ratio > 4 or aspect_ratio < 0.25:
            res.error_status = True
            res.error_type = 'QUALITY_INEFFECTIVENESS'
            res.error_name = cls.__name__
            res.error_reason = 'Image size is not valid, the ratio of width to height: ' + str(aspect_ratio)
        img.close()
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', ['img'])
class ImageQuality(BaseRule):
    """check whether image quality is good."""
    custom_config = DynamicRuleConfig(threshold = 5.5)

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        if isinstance(input_data.image[0], str):
            img = Image.open(input_data.image[0])
        else:
            img = input_data.image[0]
        device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        iqa_metric = pyiqa.create_metric('nima', device=device)
        score_fr = iqa_metric(img)
        score = score_fr.item()
        if score < cls.custom_config.threshold:
            res.error_status = True
            res.error_type = 'QUALITY_INEFFECTIVENESS'
            res.error_name = cls.__name__
            res.error_reason = 'Image quality is not satisfied, ratio: ' + str(score)
        return res

# @Model.rule_register('QUALITY_SECURITY', [])
# class ImageQRCode(BaseRule):
#     """check whether image contains QR code."""
#     @classmethod
#     def eval(cls, input_data: MetaData) -> ModelRes:
#         res = ModelRes()
#         img = cv2.imread(input_data.content)
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         scanner = zbar.Scanner()
#         tmp = scanner.scan(gray)
#         if len(tmp) != 0:
#             if tmp[0].type == 'QR-Code':
#                 res.error_status = True
#                 res.error_reason = tmp[0].data
#         return res
