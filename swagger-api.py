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

def generate_prompt_input(value):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "这是一个能够将文本翻译成中文的AI助手。请将引号中的文本翻译成简体中文。"},
            {"role": "user", "content": f"'{value}'\n 中文翻译: "},
        ],
        max_tokens=4096,
        temperature=0,
    )
    return response.choices[0]["message"]["content"].strip().replace("", "").replace("", "")


def process_item(item):
    processed_item = {}
    for key, value in item.items():
        if value:
            translated_value = generate_prompt_input(value)
            processed_item[key] = translated_value
        else:
            processed_item[key] = ''
    return processed_item


def save_item(item, file_name):
    with open(file_name, 'w') as f:
        json.dump(item, f, ensure_ascii=False, indent=4)

def process_swagger(item, i):
    print(item)
        # translated_item = process_item(swagger_file['string'])
        # save_item(translated_item, f"swagger_output/swagger{i}.json")


def main(**kwargs):
    with open('swagger-merged.json', 'r') as f:
        data = json.load(f)

    print(encode_prompt([{
        "instruction": "Please according the following apis, to create the user stories of this software system in backend.",
        "input": "\nGET get_student_by_id(student_id: number) /student/{student_id} gets student\nDELETE delete_student(student_id: number) /student/{student_id} gets student\nPOST add_student() /student Add a new student",
        "output": "As a user, I want to get student by id, so that I can get the student information.\nAs a user, I want to delete student by id, so that I can delete the student information.\nAs a user, I want to add a new student, so that I can add a new student to the system."
    }]))
    #
    # with ThreadPoolExecutor(max_workers=1) as executor:
    #     futures = {executor.submit(process_swagger, item, i) for i, item in enumerate(data)}


if __name__ == "__main__":
    main()