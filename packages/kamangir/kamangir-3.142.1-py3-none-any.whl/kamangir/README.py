import os
from blueness import module
from abcli import file
from abcli.plugins.README import build as build_README
from kamangir import NAME, VERSION, REPO_NAME, ICON
from kamangir.content import content
from kamangir.logger import logger

MY_NAME = module.name(__file__, NAME)


def build():
    logger.info(
        "{}.build {} item(s): {}".format(
            MY_NAME,
            len(content["items"]),
            ", ".join(list(content["items"].keys())),
        )
    )

    items = [
        "{}[`{}`]({}) [![image]({})]({}) {} {}".format(
            item["icon"],
            item["name"].replace("_", "-"),
            f"https://github.com/kamangir/{name}",
            item["image"],
            f"https://github.com/kamangir/{name}",
            item["description"],
            item["pypi"],
        )
        for name, item in content["items"].items()
        if name != "template"
    ]

    return build_README(
        items=items,
        cols=content["cols"],
        path=os.path.join(file.path(__file__), ".."),
        ICON=ICON,
        NAME=NAME,
        VERSION=VERSION,
        REPO_NAME=REPO_NAME,
    )
