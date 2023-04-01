import openai
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import os
import re
import fire

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

create_user_story_prompt = "You are a BA in a agile Team.Please according the input apis, to create the user stories of this software system in backend. 用户故事的模板如下：\n    \n    \"\"\"\n    用户故事：可以选择宝贝出行服务\n    作为 莉莉妈\n    我想 在滴滴打车的手机客户端里选择宝贝出行服务\n    以便于 我能够带宝宝打车出行的时候打到有儿童座椅的车\n    AC 1:  莉莉妈可以选择宝贝出行服务\n        假设 xxx\n        当 xxx\n        于是 xxx\n    \"\"\"\n"

def prompt_gpt35(prompt, value):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f'{value}'},
        ]
    )

    return response.choices[0]["message"]["content"].strip().replace("", "").replace("", "")
def prompt_davinci(value):

    response = openai.Completion.create(
        model="text-davinci-003",
        temperature=0,
        prompt=create_api_prompt + f'{value}'
    )

    return response.choices[0]["text"].strip().replace("", "").replace("", "")


def save_item(item, file_name):
    with open(file_name, 'w') as f:
        json.dump(item, f, ensure_ascii=False, indent=4)

def process_swagger(item, i):
    print("processing: ", i)
    output = prompt_gpt35(create_user_story_prompt, item['string'])
    translated_item = {
        "instruction": create_user_story_prompt,
        "input": item['string'],
        "output": output
    }
    save_item(translated_item, f"swagger_output/swagger{i}.json")

def swagger_to_userstory():
    with open('swagger-list.json', 'r') as f:
        data = json.load(f)

    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = {executor.submit(process_swagger, item, i) for i, item in enumerate(data)}


#  merge swagger_output/*.json to one jsonl file
def merge_swagger_output():
    walkdir = os.walk('swagger_output')
    with open('swagger_output.jsonl', 'w') as out_file:
        for root, dirs, files in walkdir:
            for file in files:
                if file.endswith('.json'):
                    # format json to one line
                    with open(os.path.join(root, file), 'r') as f:
                        data = json.load(f)
                        json.dump(data, out_file)
                        out_file.write('\n')

def userstory_to_swagger():
    data = [json.loads(l) for l in open('swagger_output.jsonl', "r")]

    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = {executor.submit(process_userstory, item, i) for i, item in enumerate(data)}

def process_userstory(item, i):
    # read create_api_prompt.txt.txt as the prompt
    create_api_prompt = open("create_api_prompt.txt").read() + "\n"

    print("processing user story: ", i)
    # the input will be the output of the previous task
    output = prompt_gpt35(create_api_prompt, item['output'])
    translated_item = {
        "instruction": create_api_prompt,
        "input": item['output'],
        "output": output
    }
    save_item(translated_item, f"userstory_output/userstory{i}.json")

def main(task, **kwargs):
    if not os.path.exists('userstory_output'):
        os.makedirs('userstory_output')
    if not os.path.exists('swagger_output'):
        os.makedirs('swagger_output')
    globals()[task](**kwargs)


if __name__ == "__main__":
    fire.Fire(main)
