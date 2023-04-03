"""
python -m user-story create_user_story_map
"""

import csv
import json
import os
import re

import openai
import fire
import tqdm
import time


def init_domains():
    domains = []
    with open("data/website.csv") as fd:
        rd = csv.reader(fd, delimiter=",", quotechar='"')
        for row in rd:
            if len(row) > 1:
                domains.append(row[1])

    return domains


output_dir = 'userstory_map'


def create_user_story_map():
    domains = init_domains()

    os.makedirs(output_dir, exist_ok=True)

    idx = 1

    total = len(domains)
    progress_bar = tqdm.tqdm(total=total)

    with open("prompts/user-story.md", 'r') as file:
        base_prompt = file.read()

    for domain in domains:
        if os.path.exists(f"{output_dir}/{idx}.json"):
            idx = idx + 1
            progress_bar.update()
            continue

        prompt = base_prompt.replace("${domain}", domain)

        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0,
                max_tokens=3096,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=["\"\"\""]
            )

            res = response['choices'][0]['text']
            progress_bar.update()

            output = {
                "input": domain,
                "output": res
            }

            # write to file in test_to_code
            with open(f"{output_dir}/{idx}.json", 'w') as file:
                json.dump(output, file)

            # sleep_time = 3
            # time.sleep(sleep_time)
            idx = idx + 1
        except Exception as e:
            print(e)
            print("Error, sleeping for 5 minutes")
            time.sleep(300)
            continue


def user_story_format():
    # load all files under userstory_map/{*.json}
    # parse each file
    with open("userstory_map/1.json") as file:
        parse_user_story(json.load(file))


# input(domain, map)
# domain:  Animation and Comics
# map: StoryMap { Animation { Display animation library, Create animation, Edit animation, Share animation, Save animation },  Comics { Display comic library, Create comic, Edit comic, Share comic, Save comic } }

def parse_user_story(json):
    domain = json['input']
    output_str = json['output']
    result = parse_string(output_str)
    print(result)


def parse_string(s):
    # 使用正则表达式来匹配大括号内的内容
    pattern = r"\{\s*([^{}]+)\s*\}"
    matches = re.findall(pattern, s)

    result = {}

    for match in matches:
        sections = re.split(r"\s*,\s*", match.strip())

        sub_dict = {}

        for section in sections:
            sub_dict[section] = None

        parent_match = re.search(r"^\s*([^\s]+)\s*", match)

        if parent_match:
            parent = parent_match.group(1)
            result[parent] = sub_dict

    return result


def main(task, **kwargs):
    globals()[task](**kwargs)


if __name__ == "__main__":
    fire.Fire(main)
