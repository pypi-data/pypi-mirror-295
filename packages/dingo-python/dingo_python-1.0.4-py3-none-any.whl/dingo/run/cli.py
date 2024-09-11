import pprint
import argparse
import prettytable as pt

from dingo.io import InputArgs
from dingo.model import Model
from dingo.exec import Executor, ExecProto
from dingo.utils import log


def parse_args():
    parser = argparse.ArgumentParser("dingo run with local script. (CLI)")
    parser.add_argument("-n", "--task_name", type=str,
                        default=None, help="Input task name")
    parser.add_argument("-i", "--input_path", type=str,
                        default=None, help="Input file or directory path")
    parser.add_argument("--output_path", type=str,
                        default=None, help="Output file or directory path")
    parser.add_argument("--data_format", type=str,
                        default=None, choices=['json', 'jsonl', 'listjson', 'plaintext'],
                        help="Dataset format (in ['json', 'jsonl', 'listjson', 'plaintext']), default is 'json'")
    parser.add_argument("--dataset", type=str,
                        default=None, choices=['hugging_face', 'local', 'spark'],
                        help="Dataset type (in ['hugging_face', 'local', 'spark']), default is 'hugging_face'")
    parser.add_argument("--datasource", type=str,
                        default=None, choices=['', 'hugging_face', 'local', 's3'],
                        help="Datasource (in ['hugging_face', 'local', 's3']), default is 'hugging_face'")
    parser.add_argument("--huggingface_split", type=str,
                        default=None, help="Huggingface split, default is 'train'")
    parser.add_argument("--huggingface_config_name", type=str,
                        default=None, help="Huggingface config name")
    parser.add_argument("--custom_config_path", type=str,
                        default=None, help="Custom config file path")
    parser.add_argument("--column_id", type=str, default=None,
                        help="Column name of id in the input file. If exists multiple levels, use ',' separate")
    parser.add_argument("--column_prompt", type=str, default=None,
                        help="Column name of prompt in the input file. If exists multiple levels, use ',' separate")
    parser.add_argument("--column_content", type=str, default=None,
                        help="Column name of content in the input file. If exists multiple levels, use ',' separate")
    parser.add_argument("--column_image", type=str, default=None,
                        help="Column name of image in the input file. If exists multiple levels, use ',' separate")
    parser.add_argument("-e", "--eval_models", type=str, action='append', default=None,
                        help="Eval models, can be specified multiple times like '-e default' or '-e pretrain'")

    # Warning: arguments bellow are not associated with inner abilities.
    parser.add_argument("--executor", type=str,
                        default="local", choices=["local", "spark"],
                        help="Choose the executor, default is 'local', choose in ['local', 'spark']")
    parser.add_argument("--log_level", type=str,
                        default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                        help="Choose the logging level in [\"DEBUG\", \"INFO\", " +
                             "\"WARNING\", \"ERROR\"], default is 'info'")
    return parser.parse_args()


def str_to_list(s):
    if s is None:
        return []
    return s.split(",")


if __name__ == '__main__':
    args = parse_args()
    log.setLevel(args.log_level)

    if not args.eval_models:
        print("\n=========+++ Help +++==========")
        print("Eval models not specified")
        print("\n========= Rule Model ==========")
        print("You can use '-e default' or '-e pretrain' to run all eval models\n")
        print([i for i in Model.get_rule_groups().keys()])
        print("=================================")
        print("Rule Model details are as follows: \n")
        for i in Model.get_rule_groups():
            tb = pt.PrettyTable()
            tb.field_names = ["ModelName", "Rules"]
            tb.add_row([i, ",\n".join([str(j.__name__).split('.')[-1] for j in Model.get_rule_groups()[i]])])
            print(tb)
        print("=================================")
        print("Or combine them with a json file select from this list\n")
        Model.print_rule_list()
        print("=================================")
        print("\n")
        print("=========== LLM Model ===========")
        print(",".join([i for i in Model.llm_models.keys()]))
        print("=================================")
        print("\n")

    else:
        # parse input
        item = InputArgs()
        if args.task_name:
            item.task_name = args.task_name
        if args.eval_models:
            item.eval_models = args.eval_models
        if args.input_path:
            item.input_path = args.input_path
        if args.output_path:
            item.output_path = args.output_path
        if args.data_format:
            item.data_format = args.data_format
        if args.dataset:
            item.dataset = args.dataset
        if args.datasource:
            item.datasource = args.datasource
        if args.huggingface_split:
            item.huggingface_split = args.huggingface_split
        if args.huggingface_config_name:
            item.huggingface_config_name = args.huggingface_config_name
        if args.column_id:
            item.column_id = str_to_list(args.column_id)
        if args.column_prompt:
            item.column_prompt = str_to_list(args.column_prompt)
        if args.column_content:
            item.column_content = str_to_list(args.column_content)
        if args.column_image:
            item.column_image = str_to_list(args.column_image)
        if args.custom_config_path:
            item.custom_config_path = args.custom_config_path

        # Get custom rule config
        Model.apply_config(item.custom_config_path)
        log.debug("Load custom config.")

        # Init
        executor: ExecProto = Executor.exec_map[args.executor](item)

        # Evaluate
        record_list = executor.execute()
        log.info("========= ↓ Evaluation result ↓ =========")
        pprint.pprint(record_list, indent=4, sort_dicts=False)
