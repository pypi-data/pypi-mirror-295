from typing import Callable, List, Generator, Union, Any, Dict
import os
import time
import uuid

from pyspark.rdd import RDD
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, Row, DataFrame

from dingo.exec.base import Executor
from dingo.data import dataset_map, datasource_map, Dataset
from dingo.config import GlobalConfig
from dingo.model import Model
from dingo.model.modelres import ModelRes
from dingo.model.rule.base import BaseRule
from dingo.io import InputArgs, MetaData, SummaryModel, ErrorInfo
from dingo.utils import log

QUALITY_MAP = Model.rule_metric_type_map


@Executor.register('spark')
class SparkExecutor(Executor):
    """
    Spark executor
    """

    def __init__(self, input_args: InputArgs,
                 spark_rdd: RDD = None,
                 spark_session: SparkSession = None,
                 spark_conf: SparkConf = None,
                 clean_context: bool = True):
        # eval param
        self.model_type = None
        self.model_name = None
        self.model = None
        self.summary = None
        self.error_info_list = None

        # init param
        self.input_args = input_args
        self.spark_rdd = spark_rdd
        self.spark_session = spark_session
        self.spark_conf = spark_conf

        # run param
        self.clean_context = clean_context

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['spark_session']
        del state['spark_rdd']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def load_data(self) -> Generator[Any, None, None]:
        """
        Reads data from given path. Returns generator of raw data.

        **Run in executor.**

        Returns:
            Generator[Any, None, None]: Generator of raw data.
        """
        new_input_args = self.input_args
        dataset_type = "spark"
        source = self.input_args.datasource if self.input_args.datasource != "" else self.input_args.dataset
        dataset_cls = dataset_map[dataset_type]
        dataset: Dataset = dataset_cls(source=datasource_map[source](input_args=new_input_args))
        return dataset.get_data()

    def execute(self):
        current_time = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        print("============= Init pyspark =============")
        if self.spark_session is not None:
            spark = self.spark_session
            sc = spark.sparkContext
        elif self.spark_conf is not None:
            spark = SparkSession.builder.config(conf=self.spark_conf).getOrCreate()
            sc = spark.sparkContext
        else:
            spark = SparkSession.builder.master(
                "spark://127.0.0.1:7077").appName(f"Dingo_Data_Evaluation_{current_time}").getOrCreate()
            sc = spark.sparkContext
        print("============== Init Done ===============")

        try:
            # Model init
            if len(self.input_args.eval_models) != 1:
                raise RuntimeError("Len of Spark evaluation model must be 1.")
            self.get_model_list(self.input_args.eval_models[0])

            # Exec Eval
            if self.spark_rdd is not None:
                data_rdd = self.spark_rdd
            else:
                data_rdd = sc.parallelize(self.load_data(), 3)
            total = data_rdd.count()

            error_info_list = data_rdd.map(self.evaluate)
            _error_info_list = error_info_list.filter(lambda x: False if len(x['error_type']) == 0 else True)
            _error_info_list.cache()

            num_bad = _error_info_list.count()
            self.error_info_list = _error_info_list
            # calculate count
            self.summary = SummaryModel(
                task_id=str(uuid.uuid1()),
                task_name=self.input_args.task_name,
                eval_model=self.model_name,
                input_path=self.input_args.input_path,
                output_path=self.input_args.output_path,
                create_time=time.strftime('%Y%m%d_%H%M%S', time.localtime()),
                score=0,
                num_good=0,
                num_bad=0,
                total=0,
                error_type_ratio={q_s: 0 for q_s in QUALITY_MAP},
                error_name_ratio={}
            )
            self.summary.total = total
            self.summary.num_bad = num_bad
            self.summary.num_good = total - num_bad
            self.summary.score = round(self.summary.num_good / self.summary.total * 100, 2)

            self.summarize()
        except Exception as e:
            raise e
        finally:
            if self.clean_context:
                spark.stop()
                sc.stop()
            else:
                self.spark_session = spark
        return self.summary.to_dict()

    def clean_context_and_session(self):
        sc = self.spark_session.sparkContext
        self.spark_session.stop()
        sc.stop()

    def summarize(self):
        # calculate
        for q_s in QUALITY_MAP:
            q_s_n = self.error_info_list.filter(lambda x: q_s in x['error_type']).count()
            self.summary.error_type_ratio[q_s] = round(q_s_n / self.summary.total, 6)

        rule_map = self.model
        for r in rule_map:
            r_n = get_quality_signal(r) + '-' + r.__name__
            r_n_n = self.error_info_list.filter(lambda x: r_n in x['error_name']).count()
            self.summary.error_name_ratio[r_n] = round(r_n_n / self.summary.total, 6)

    def evaluate(self, data_rdd_item) -> Dict[str, Any]:

        # eval with models ( Big Data Caution ）
        return execute_rule_spark(self.model, data_rdd_item)

    def save_data(self, start_time):
        output_path = os.path.join(self.input_args.output_path, start_time)
        model_path = os.path.join(output_path, self.model_name)
        if not os.path.exists(model_path):
            os.makedirs(model_path)

    def get_model_list(self, model_name):
        self.model_name = model_name
        log.debug(f"[GlobalConfig.config]: {GlobalConfig.config}")
        if model_name in Model.llm_models:
            log.debug(f"[Load llm model {model_name}]")
            raise RuntimeError("LLM models are not supported yet.")
        elif model_name in Model.rule_groups:
            log.debug(f"[Load rule model {model_name}]")
            self.model: List[BaseRule] = Model.rule_groups[model_name]
            model_type = 'rule'
        elif GlobalConfig.config and GlobalConfig.config.custom_rule_list:
            log.debug("[Load custom rule]")
            self.model: List[BaseRule] = []
            for rule in GlobalConfig.config.custom_rule_list:
                assert isinstance(rule, str)
                if rule not in Model.rule_name_map:
                    raise KeyError(
                        f"{rule} not in Model.rule_name_map, there are {str(Model.rule_name_map.keys())}")
                self.model.append(Model.rule_name_map[rule])
            model_type = 'rule'
        else:
            raise KeyError('no such model: ' + self.model_name)

        # record for this
        self.model_type = model_type


def get_quality_signal(rule: Callable):
    for quality_signal in QUALITY_MAP:
        for rule_class in QUALITY_MAP[quality_signal]:
            if rule.__name__ == rule_class.__name__:
                return quality_signal

    raise RuntimeError('this rule can not find its quality_signal: ' + rule.__name__)


def execute_rule_spark(rule_map, d: MetaData) -> Dict[str, Any]:
    error_info = ErrorInfo(data_id=d.data_id, prompt=d.prompt, content=d.content)

    log.debug("[RuleMap]: " + str(rule_map))
    if not isinstance(d, MetaData):
        raise TypeError(f'input data must be an instance of MetaData: {str(d)}')
    for r in rule_map:
        rule_name = r.__name__
        # execute rule
        tmp: ModelRes = r.eval(d)
        # analyze result
        if not tmp.error_status:
            continue

        if tmp.error_type not in error_info.error_type:
            error_info.error_type.append(tmp.error_type)
        error_info.error_name.append(tmp.error_type + '-' + rule_name)
        error_info.error_reason.append(tmp.error_reason)
    return error_info.to_dict()
