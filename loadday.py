#!/usr/bin/env python

import sys
import logging
import json
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(sys.argv[0])

loader_code = """with open("inputs/{day:02d}.txt") as infile:
    for line in infile.read().splitlines():
        pass"""

notebook_template = {
    "cells": [
        {"cell_type": "markdown", "metadata": {"function": "day-desc-1"}, "source": []},
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [],
        },
        {
            "cell_type": "markdown",
            "metadata": {"function": "day-desc-2"},
            "source": ["# Here goes Part 2 Code\n", "**Do not change**"],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [],
        },
    ],
}


def get_input(day, token):
    input_url = f"https://adventofcode.com/2021/day/{day}/input"
    puzzle_input = requests.get(input_url, cookies={"session": token}).text
    with open(f"inputs/{day:02d}.txt", "w") as input_file:
        input_file.write(puzzle_input)


def get_task_descriptions(day, token):
    description_url = f"https://adventofcode.com/2021/day/{day}"
    task_page = requests.get(description_url, cookies={"session": token}).text
    soup = BeautifulSoup(task_page, "html.parser")
    return [
        desc.prettify()
        for desc in soup.find_all("article", attrs={"class": "day-desc"})
    ]


def create_notebook(day, file, part1_description):
    notebook_content = notebook_template.copy()
    notebook_content["cells"][0]["source"] = [part1_description]

    loader_code_content = loader_code.format(day=day)

    notebook_content["cells"][1]["source"] = loader_code_content.splitlines()

    with open(file, "w") as notebook_file:
        json.dump(notebook_content, notebook_file)


def add_part2_description(file, part2_description):
    with open(file, "r") as old_notebook_file:
        notebook_content = json.load(old_notebook_file)

    for cell in notebook_content["cells"]:
        if (
            "function" in cell["metadata"]
            and cell["metadata"]["function"] == "day-desc-2"
        ):
            cell["source"] = [part2_description]
            break

    with open(file, "w") as notebook_file:
        json.dump(notebook_content, notebook_file)


def main():
    current_day = date.today().day
    notebook = Path(f"{current_day:02d}.ipynb")

    try:
        with open(".session_token") as tokenfile:
            token = tokenfile.read().strip()
    except (FileNotFoundError, PermissionError) as e:
        logger.error(".session_token not found", e)

    descriptions = get_task_descriptions(current_day, token)

    if not notebook.exists():
        get_input(current_day, token)
        create_notebook(current_day, notebook, descriptions[0])
    else:
        add_part2_description(notebook, descriptions[1])


if __name__ == "__main__":
    main()
