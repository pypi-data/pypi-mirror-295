from typing import Callable, List, Generator
import os
import time
import json
import uuid

from dingo.exec.base import Executor
from dingo.data import dataset_map, datasource_map, Dataset
from dingo.config import GlobalConfig
from dingo.model import Model
from dingo.model.modelres import ModelRes
from dingo.model.llm.base import BaseLLM
from dingo.model.rule.base import BaseRule
from dingo.io import InputArgs, MetaData, SummaryModel, ErrorInfo
from dingo.utils import log

QUALITY_MAP = Model.rule_metric_type_map


@Executor.register('local')
class LocalExecutor(Executor):

    def __init__(self, input_args: InputArgs):
        self.input_args = input_args

    def load_data(self) -> Generator[MetaData, None, None]:
        """
        Reads data from given path.

        **Run in executor.**

        Returns:
            Generator[MetaData]
        """
        new_input_args = self.input_args
        dataset_type = self.input_args.dataset
        source = self.input_args.datasource if self.input_args.datasource != "" else dataset_type
        dataset_cls = dataset_map[dataset_type]
        dataset: Dataset = dataset_cls(source=datasource_map[source](input_args=new_input_args))
        return dataset.get_data()

    def execute(self) -> List[SummaryModel]:
        """
        Executes given input models.

        Returns:

        """
        return self.evaluate()

    def summarize(self, record) -> SummaryModel:
        pass

    def get_score(self, path, summary, error_info_list, model, model_type):
        """
        get score (main progres).
        Args:

            path (Any): _description_
            summary (Any): _description_
            error_info_list (Any): _description_
            model (Any): _description_
            model_type (str): _description_
        """
        log.debug('[get_score]:' + path)
        data_iter = self.load_data()

        for data in data_iter:
            executor(model_type)(summary, error_info_list, model, data)
            summary.total += 1

        log.debug('[Summary]: ' + str(summary))
        calculate_ratio(summary, model_type)
        log.debug('[Summary]: ' + str(summary))

    def evaluate(self) -> List[SummaryModel]:
        if len(self.input_args.eval_models) != 1:
            raise RuntimeError("Len of evaluation model must be 1.")
        current_time = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        input_path = self.input_args.input_path
        output_path = os.path.join(self.input_args.output_path, current_time)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        summary_list = []
        custom = False
        log.debug(str(self.input_args.eval_models))
        for model_name in self.input_args.eval_models:
            log.debug(f"[GlobalConfig.config]: {GlobalConfig.config}")
            if model_name in Model.llm_models:
                log.debug(f"[Load llm model {model_name}]")
                model = Model.llm_models[model_name]
                model_type = 'llm'
            elif model_name in Model.rule_groups:
                log.debug(f"[Load rule model {model_name}]")
                model: List[BaseRule] = Model.rule_groups[model_name]
                model_type = 'rule'
            elif GlobalConfig.config and GlobalConfig.config.custom_rule_list:
                log.debug("[Load custom rule]")
                custom = True
                model: List[BaseRule] = []
                for rule in GlobalConfig.config.custom_rule_list:
                    assert isinstance(rule, str)
                    if rule not in Model.rule_name_map:
                        raise KeyError(
                            f"{rule} not in Model.rule_name_map, there are {str(Model.rule_name_map.keys())}")
                    model.append(Model.rule_name_map[rule])

                model_type = 'rule'
            else:
                raise KeyError('no such model: ' + model_name)
            log.debug("[ModelType]: " + model_type)
            model_path = output_path + '/' + model_name
            if not os.path.exists(model_path):
                os.makedirs(model_path)

            summary = SummaryModel(
                task_id=str(uuid.uuid1()),
                task_name=self.input_args.task_name,
                eval_model=model_name,
                input_path=input_path,
                output_path=output_path,
                create_time=time.strftime('%Y%m%d_%H%M%S', time.localtime()),
                score=0,
                num_good=0,
                num_bad=0,
                total=0,
                error_type_ratio={q_s : 0 for q_s in QUALITY_MAP},
                error_name_ratio={}
            )
            error_info_list = []
            self.get_score(input_path, summary, error_info_list, model, model_type)

            # pprint.pprint(record, sort_dicts=False)
            if model_type in ['rule','llm']:
                write_data(summary, error_info_list, model_path)
            else:
                raise KeyError('no such model: ' + model_type)

            summary_list.append(summary)
            if custom:
                break
        log.debug(summary_list)
        return summary_list


def get_quality_signal(rule: Callable):
    for quality_signal in QUALITY_MAP:
        for rule_class in QUALITY_MAP[quality_signal]:
            if rule.__name__ == rule_class.__name__:
                return quality_signal

    raise RuntimeError('this rule can not find its quality_signal: ' + rule.__name__)


def write_data(summary: SummaryModel, error_info_list: List, path):
    for q_s in QUALITY_MAP:
        q_s_p = os.path.join(path, q_s)
        os.makedirs(q_s_p)

    for error_info in error_info_list:
        for e_n in error_info.error_name:
            q_s = str(e_n).split('-')[0]
            r_n = str(e_n).split('-')[1]
            f_n = os.path.join(path, q_s, r_n) + ".jsonl"
            with open(f_n, 'a', encoding='utf-8') as f:
                str_json = json.dumps(error_info.to_dict(), ensure_ascii=False)
                f.write(str_json + '\n')
    with open(path + '/summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary.to_dict(), f, indent=4, ensure_ascii=False)


def execute_rule(summary: SummaryModel, error_info_list: List, rule_map, d: MetaData):
    if_good = True
    error_info = ErrorInfo(data_id=d.data_id, prompt=d.prompt, content=d.content)
    log.debug("[RuleMap]: " + str(rule_map))
    for r in rule_map:
        r_n = r.__name__
        # execute rule
        tmp: ModelRes = r.eval(d)
        # analyze result
        if tmp.error_status is False:
            continue
        if_good = False
        if tmp.error_type not in error_info.error_type:
            error_info.error_type.append(tmp.error_type)
        error_info.error_name.append(tmp.error_type + '-' + r_n)
        error_info.error_reason.append(tmp.error_reason)

    if not if_good:
        error_info_list.append(error_info)
        summary.num_bad += 1
        for q_s in error_info.error_type:
            summary.error_type_ratio[q_s] += 1
        for e_n in error_info.error_name:
            if e_n not in summary.error_name_ratio:
                summary.error_name_ratio[e_n] = 0
            summary.error_name_ratio[e_n] += 1


def execute_llm(summary: SummaryModel, error_info_list: List, llm: BaseLLM, d: MetaData):
    error_info = ErrorInfo(data_id=d.data_id, prompt=d.prompt, content=d.content)
    tmp: ModelRes = llm.call_api(d)
    if tmp.error_status is False:
        return

    if tmp.error_type not in error_info.error_type:
        error_info.error_type.append(tmp.error_type)
    error_info.error_name.append(tmp.error_type + '-' + tmp.error_name)
    error_info.error_reason.append(tmp.error_reason)

    error_info_list.append(error_info)
    summary.num_bad += 1
    for q_s in error_info.error_type:
        summary.error_type_ratio[q_s] += 1
    for e_n in error_info.error_name:
        if e_n not in summary.error_name_ratio:
            summary.error_name_ratio[e_n] = 0
        summary.error_name_ratio[e_n] += 1


def calculate_ratio(summary: SummaryModel, model_type):
    summary.num_good = summary.total - summary.num_bad
    summary.score = round(summary.num_good / summary.total * 100, 2)
    for q_s in summary.error_type_ratio:
        summary.error_type_ratio[q_s] = round(summary.error_type_ratio[q_s] / summary.total, 6)
    for e_n in summary.error_name_ratio:
        summary.error_name_ratio[e_n] = round(summary.error_name_ratio[e_n] / summary.total, 6)


def executor(model_type: str) -> Callable:
    if model_type == 'rule':
        return execute_rule
    if model_type == 'llm':
        return execute_llm
    raise RuntimeError(f'Unsupported model type: {model_type}')


# def write_data(model_type: str) -> Callable:
#     if model_type == 'rule':
#         return write_data_rule
#     if model_type == 'llm':
#         return write_data_llm
