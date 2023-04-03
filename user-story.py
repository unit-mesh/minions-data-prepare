"""
python -m user-story create_user_story_map
"""

import csv
import json
import os
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
                domains.append(row[1] + " Website")

    return domains


output_dir = 'userstory_map'


def create_user_story_map():
    domains = init_domains()

    os.makedirs(output_dir, exist_ok=True)

    # open test_code_code.md
    base_prompt = open("test_to_code.md").read() + "\n"

    idx = 1

    total = len(domains)
    progress_bar = tqdm.tqdm(total=total)

    for domain in domains:
        # if output file exists, skip
        if os.path.exists(f"{output_dir}/{idx}.json"):
            idx = idx + 1
            progress_bar.update()
            continue

        prompt = f"Design a #User story mapping# for { domain } based on your understanding. The format for the " \
                 f"user story map is as follows: ###map {{ Before boarding {{ Display unsupported orders, " \
                 f"Select travel time, ... }} On Board {{...}} }} ###"

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

            output = response['choices'][0]['text']
            progress_bar.update()

            output = {
                "input": domain,
                "output": output
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


def main(task, **kwargs):
    globals()[task](**kwargs)


if __name__ == "__main__":
    fire.Fire(main)

