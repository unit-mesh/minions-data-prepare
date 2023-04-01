"""
python -m swagger-user-story swagger_to_userstory
python -m swagger-user-story userstory_to_swagger

"""
import json
import os
import openai
import fire
import tqdm
import time

import utils
from utils import json_to_jsonl

jsonl_path = 'test_to_code.jsonl'
output_dir = 'test_to_code'


def merge_test_to_jsonl():
    source = 'test-api'
    target = jsonl_path

    walkdir = os.walk(source)

    index = 0
    with open(target, 'w') as out_file:
        for root, dirs, files in walkdir:
            for file in files:
                if file.endswith('.json'):
                    # format json to one line
                    with open(os.path.join(root, file), 'r') as f:
                        data = json.load(f)
                        data['id'] = 'task_' + str(index)
                        json.dump(data, out_file)
                        out_file.write('\n')


def merge_test_output_to_jsonl():
    json_to_jsonl(output_dir, "test_to_code_output.jsonl", ".json")


def generate_code_from_tests():
    tasks = []
    with open(jsonl_path, 'r') as file:
        for line in file:
            tasks.append(json.loads(line))

    print(f"Loaded {len(tasks)} tasks")

    os.makedirs(output_dir, exist_ok=True)

    request_idx = 0

    machine_instruction_data = []

    progress_bar = tqdm.tqdm(total=100)
    if machine_instruction_data:
        progress_bar.update(len(machine_instruction_data))

    # open test_code_code.md
    base_prompt = open("test_to_code.md").read() + "\n"

    idx = 1

    total = len(tasks)
    for task in tasks:
        prompt = f"{base_prompt}\n class information: ### {task['classInfo']} \n ### test code: ### {task['testMethod']} \n ###"

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\"\"\""]
        )

        code = response['choices'][0]['text']
        progress_bar.update(idx / total * 100)

        output = {
            "classInfo": task['classInfo'],
            "testMethod": task['testMethod'],
            "code": code
        }

        # write to file in test_to_code
        with open(f"{output_dir}/{idx}.json", 'w') as file:
            json.dump(output, file)

        sleep_time = 10
        time.sleep(sleep_time)
        idx = idx + 1


def main(task, **kwargs):
    globals()[task](**kwargs)


if __name__ == "__main__":
    fire.Fire(main)
