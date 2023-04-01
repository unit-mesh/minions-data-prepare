import openai
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import os
import re

def encode_prompt(prompt_instructions):
    """Encode multiple prompt instructions into a single string."""
    prompt = open("prompt_cn.txt").read() + "\n"

    for idx, task_dict in enumerate(prompt_instructions):
        (instruction, input, output) = task_dict["instruction"], task_dict["input"], task_dict["output"]
        instruction = re.sub(r"\s+", " ", instruction).strip().rstrip(":")
        input = "<noinput>" if input.lower() == "" else input
        prompt += f"###\n"
        prompt += f"{idx + 1}. Instruction: {instruction}\n"
        prompt += f"{idx + 1}. Input:\n{input}\n"
        prompt += f"{idx + 1}. Output:\n{output}\n"
    prompt += f"###\n"
    prompt += f"{idx + 2}. Instruction:"
    return prompt

instruction = "You are a BA in a agile Team.Please according the input apis, to create the user stories of this software system in backend. 用户故事的模板如下：\n    \n    \"\"\"\n    用户故事：可以选择宝贝出行服务\n    作为 莉莉妈\n    我想 在滴滴打车的手机客户端里选择宝贝出行服务\n    以便于 我能够带宝宝打车出行的时候打到有儿童座椅的车\n    AC 1:  莉莉妈可以选择宝贝出行服务\n        假设 xxx\n        当 xxx\n        于是 xxx\n    \"\"\"\n"

def generate_prompt_input(value):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": f'{value}'},
        ]
    )

    return response.choices[0]["message"]["content"].strip().replace("", "").replace("", "")


def save_item(item, file_name):
    with open(file_name, 'w') as f:
        json.dump(item, f, ensure_ascii=False, indent=4)

def process_swagger(item, i):
    print("processing: ", i)
    output = generate_prompt_input(item['string'])
    translated_item = {
        "instruction": instruction,
        "input": item['string'],
        "output": output
    }
    save_item(translated_item, f"swagger_output/swagger{i}.json")

def main(**kwargs):
    with open('swagger-list.json', 'r') as f:
        data = json.load(f)

    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = {executor.submit(process_swagger, item, i) for i, item in enumerate(data)}


if __name__ == "__main__":
    main()