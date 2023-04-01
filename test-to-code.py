"""
python -m swagger-user-story swagger_to_userstory
python -m swagger-user-story userstory_to_swagger

"""
import json
import os
import fire
import openai
import tqdm
from utils import json_to_jsonl

jsonl_path = 'test_to_code.jsonl'
output_dir = 'test_to_code'


def merge_test_to_jsonl():
    json_to_jsonl('test-api', jsonl_path, ".prompt")


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

    # create output dir
    os.makedirs(output_dir, exist_ok=True)

    index = 0
    for task in tasks:
        print(f"execute task {index}")
        prompt = f"{base_prompt}\n class information: ### {task['classInfo']} \n ### test code: ### {task['testMethod']} \n ###"
        response = prompt_davinci(prompt)

        output = {
            "classInfo": task['classInfo'],
            "testMethod": task['testMethod'],
            "code": response
        }

        # write to file in test_to_code
        with open(f"{output_dir}/{index}.json", 'w') as file:
            json.dump(output, file)

        index += 1


def prompt_davinci(value):
    response = openai.Completion.create(
        model="text-davinci-003",
        temperature=0,
        prompt=f'{value}'
    )

    return response.choices[0]["text"].strip().replace("", "").replace("", "")


def main(task, **kwargs):
    globals()[task](**kwargs)


if __name__ == "__main__":
    fire.Fire(main)
