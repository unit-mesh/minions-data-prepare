"""
python -m swagger-user-story swagger_to_userstory
python -m swagger-user-story userstory_to_swagger

"""
import openai
import json
from concurrent.futures import ThreadPoolExecutor
import os
import re
import fire
from tqdm import tqdm

from utils import json_to_jsonl


def merge_test_to_jsonl():
#     load all prompts(json) in test-api/ and merge to json
    json_to_jsonl('test-api', 'test_to_code.jsonl', ".prompt")

def generate_code_from_tests():
    pass


def main(task, **kwargs):
    globals()[task](**kwargs)


if __name__ == "__main__":
    fire.Fire(main)
