import subprocess
import sys
import os
import json

packages = [
    "py-cord"
]

files = {
    "datas/bot.json": {
        "bot_token": None,
        "version": "1.0.0",
        "default_prefix": "+",
        "cogs_folder": "cogs",
        "logs_folder": "datas/logs",
        "beta_guilds": [],
        "debug_mode": True
    }
}

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
def create_file(filepath, filedata):
    dirname = os.path.dirname(filepath)
    if not os.path.exists(dirname): os.makedirs(dirname)

    with open(filepath, "w") as f:
        json.dump(filedata, f, indent=4)


if __name__ == "__main__":
    for package in packages:
        install(package)
    for filepath in files:
        create_file(filepath, files[filepath])
    
    print("check datas/bot.json file to configure your bot token and other stuff")
    