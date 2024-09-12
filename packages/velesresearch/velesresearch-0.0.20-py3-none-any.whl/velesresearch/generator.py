"Functions for generating survey package."
from __future__ import annotations
import os
import shutil
from importlib.resources import files
from json import dump
from pathlib import Path
import fileinput
from pynpm import YarnPackage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .structure import Survey


def generate_survey(survey_object: "Survey", path: str | Path = os.getcwd()) -> None:
    if isinstance(path, str):
        path = Path(path)

    path = path / survey_object.label.casefold()

    if not os.path.exists(path / "package.json"):
        template = str(files("velesresearch.website_template"))
        shutil.copytree(
            template, path, ignore=shutil.ignore_patterns("__pycache__", "__init__.py")
        )

    if not os.path.exists(path / "node_modules"):
        YarnPackage(path).install()

    # survey.js
    with open(path / "src" / "survey.js", "w", encoding="utf-8") as survey_js:
        survey_js.write("export const json = ")

    with open(path / "src" / "survey.js", "a", encoding="utf-8") as survey_js:
        from .structure import SurveyEncoder

        dump(survey_object, survey_js, cls=SurveyEncoder)

    index_html = path / "public" / "index.html"
    new_line = f"    <title>{survey_object.title}</title>\n"

    # config.js
    shutil.copyfile(
        files("velesresearch.website_template") / "src" / "config.js",
        path / "src" / "config.js",
    )
    with open(path / "src" / "config.js", "r", encoding="utf-8") as config_js:
        if survey_object.dict().get("options"):
            number_of_groups = survey_object.options.number_of_groups
        else:
            number_of_groups = 1
        config_js_data = config_js.read()
        config_js_data = config_js_data.replace(
            r"{% numberOfGroups %}", str(number_of_groups)
        )
    with open(path / "src" / "config.js", "w", encoding="utf-8") as config_js:
        config_js.write(config_js_data)

    # index.html
    # use fileinput to modify the file
    for line in fileinput.input(index_html, inplace=True):
        if "<title>" in line and "</title>" in line:
            print(new_line, end="")
        else:
            print(line, end="")
