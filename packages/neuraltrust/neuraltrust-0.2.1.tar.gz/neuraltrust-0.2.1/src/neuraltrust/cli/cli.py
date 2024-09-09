#!/usr/bin/env python3

import argparse
from ..utils.config import ConfigHelper
from ..utils.run_helper import RunHelper
from ..utils.kwparser import KeyValueAction
from ..interfaces.model import Model
from ..loaders import LoadFormat


def main():
    parser = argparse.ArgumentParser(
        prog="neuraltrust",
        description="Evaluation framework for your LLM-powered applications",
    )

    subparsers = parser.add_subparsers(title="commands", dest="command")

    # neuraltrust init
    parser_init = subparsers.add_parser("init", help="Configure settings")
    parser_init.set_defaults(func=init)

    # neuraltrust config
    parser_config = subparsers.add_parser("config", help="Configure settings")
    parser_config.set_defaults(func=config)


    # neuraltrust run [eval_name] [kwargs]
    parser_run = subparsers.add_parser("run", help="Run an eval suite")

    # Add the 'eval_name' positional argument
    parser_run.add_argument(
        "eval_id",
        type=str,
        help="The id of the eval or eval suite to run",
    )

    # Add the 'kwargs' argument for key=value pairs
    parser_run.add_argument(
        "kwargs",
        nargs="*",
        action=KeyValueAction,
        help="Additional named arguments as key=value pairs",
    )

    # Add the '--format' optional argument
    parser_run.add_argument(
        "--model",
        type=str,
        choices=[
            Model.GPT35_TURBO.value,
            Model.GPT4.value,
            Model.GPT4_1106_PREVIEW.value,
        ],
        help="LLM model for evaluation",
    )

    # Add the '--format' optional argument
    parser_run.add_argument(
        "--format",
        type=str,
        choices=[
            LoadFormat.JSON.value,
            LoadFormat.DICT.value
        ],
        help="Output format type",
    )

    # Add the '--filename' optional argument
    parser_run.add_argument(
        "--filename",
        type=str,
        help="Path to the file",
    )

    # Set the default function to be called
    parser_run.set_defaults(func=run_delegator)

    # Parse the arguments
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


def init(args):
    """Initializes NeuralTrust and sets the necessary configuration variables"""
    config_data = ConfigHelper.load_config()

    openai_api_key = input("Enter your OpenAI API key: ")
    config_data["openai_api_key"] = openai_api_key

    neuraltrust_api_key = input("Enter your NeuralTrust API key: ")
    config_data["neuraltrust_api_key"] = neuraltrust_api_key

    config_data["llm_judge_model"] = "gpt-4o-mini"
    config_data["llm_target_model"] = "gpt-4o-mini"
    config_data["llm_provider"] = "openai"

    # Add other configuration prompts as needed

    ConfigHelper.save_config(config_data)
    print("Configuration updated successfully. See neuraltrust_config.yml for details.")


def config(args):
    """Prints the current configuration"""
    config_data = ConfigHelper.load_config()
    print(config_data)

def run_delegator(args):
    """Delegates the run command to the appropriate function"""

    if not ConfigHelper.is_set():
        print("Please run 'neuraltrust init' to configure your API keys")
        return

    # Load the eval model
    model = ConfigHelper.load_judge_llm_model()
    if args.model is not None:
        model = args.model

    # Check if both format and filename are set
    if args.eval_id is not None:
        run_batch(args.eval_id, model, format=args.format)
        return

    else:
        raise Exception("Invalid run args")


# Define the run_batch function
def run_batch(
    eval_id: str, model: str, format: str, **kwargs
):
    # Implementation for running batch process
    try:
        print(
            f"Running batch with set={eval_id}, model={model}, kwargs={kwargs}"
        )

        RunHelper.run_eval_on_batch(
            eval_id=eval_id,
            model=model,
            max_parallel_evals=5,
            **kwargs
        )
    except Exception as e:
        print(f"{e}")
        return


def run_datapoint(eval_name: str, model: str, **kwargs):
    """Runs a single eval on a single datapoint"""
    try:
        print(f"Running single with {eval_name}, model {model}, and kwargs {kwargs}")
        testset_id = "testset_id"
        RunHelper.run_eval(eval_name, testset_id, model, **kwargs)
    except Exception as e:
        print(f"{e}")
        return


if __name__ == "__main__":
    main()