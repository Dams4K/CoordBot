import sys
import os
import json

files = {
    "datas/bot.json": {
        "bot_token": None,
        "version": "1.0.0",
        "default_prefix": "+",
        "cogs_folder": "cogs",
        "logs_folder": "datas/logs",
        "beta_guilds": None,
        "debug_mode": False
    }
}

def install_packages(file_path):
    assert os.path.exists(file_path), f"{file_path} did not exist"
    os.system(f"{sys.executable} -m pip install -r {file_path}")

def create_file(filepath, filedata):
    dirname = os.path.dirname(filepath)
    if os.path.exists(filepath):
        print(f"{filepath} already exist - skipped")
        return

    if not os.path.exists(dirname): os.makedirs(dirname)

    with open(filepath, "w") as f:
        json.dump(filedata, f, indent=4)


if __name__ == "__main__":
    install_packages("requirements.txt")
    for filepath in files:
        create_file(filepath, files[filepath])
    
    print("check datas/bot.json file to configure your bot token and other stuff")
    