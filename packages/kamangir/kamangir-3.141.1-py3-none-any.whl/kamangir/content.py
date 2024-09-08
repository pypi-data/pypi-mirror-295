import abcli
import articraft
from blue_objects.env import ABCLI_PUBLIC_PREFIX
import blue_geo
import blue_objects
import blue_options
import blue_plugin
import blue_stability
import hubblescope
import ferfereh
import gizai
import notebooks_and_scripts
import openai_commands
import roofAI
import vancouver_watching

content = {
    "cols": 3,
    "items": {
        "blue-geo": {
            "module": blue_geo,
        },
        "hubble": {
            "module": hubblescope,
        },
        "vancouver-watching": {
            "module": vancouver_watching,
        },
        "roofAI": {
            "module": roofAI,
        },
        "openai-commands": {
            "module": openai_commands,
        },
        "notebooks-and-scripts": {
            "module": notebooks_and_scripts,
        },
        "giza": {
            "module": gizai,
        },
        "awesome-bash-cli": {
            "module": abcli,
        },
        "ferfereh": {
            "module": ferfereh,
        },
        "blue-options": {
            "module": blue_options,
        },
        "blue-objects": {
            "module": blue_objects,
        },
        "blue-plugin": {
            "module": blue_plugin,
        },
        "blue-stability": {
            "module": blue_stability,
        },
        "aiart": {
            "module": articraft,
        },
        "Kanata": {
            "legacy": True,
            "image": f"{ABCLI_PUBLIC_PREFIX}/Canadians_v11.gif",
            "description": "a multi-screen video feed that is comprised of a matrix of animated faces that slide to the right.",
        },
        "dec82": {
            "legacy": True,
            "image": "https://github.com/kamangir/blue-bracket/raw/main/images/dec82-6.jpg",
            "description": "A wearable Raspberry Pi + Grove / Qwiic + Camera.",
        },
        "blue-rvr": {
            "legacy": True,
            "image": "https://github.com/kamangir/blue-rvr/raw/master/abcli/assets/marquee.jpeg",
            "description": "a bash cli for Sphero RVR SDK - runs deep learning vision models on a Raspberry Pi using Python and TensorFlow.",
        },
        "blue-bracket": {
            "legacy": True,
            "image": "https://github.com/kamangir/blue-bracket/raw/main/images/marquee.jpg",
            "description": "a parametric 3d-printed bracket to build hardware for machine vision & ai on raspberry pi and jetson nano on the edge.",
        },
        "blue-sbc": {
            "legacy": True,
            "image": "https://github.com/kamangir/blue-bracket/raw/main/images/blue3-1.jpg",
            "description": "python + bash bootstrap for edge computing on single board computers.",
        },
        "template": {
            "module": abcli,
        },
    },
}

for name, item in content["items"].items():
    if "module" not in item:
        item["icon"] = ""
        item["name"] = name
        item["pypi"] = ""
        continue

    module = item["module"]
    item["description"] = module.DESCRIPTION.replace(module.ICON, "").strip()
    item["icon"] = f"{module.ICON} "
    item["image"] = module.MARQUEE
    item["name"] = module.NAME
    item["pypi"] = (
        " [![PyPI version](https://img.shields.io/pypi/v/{}.svg)](https://pypi.org/project/{}/)".format(
            module.NAME, module.NAME
        )
    )
