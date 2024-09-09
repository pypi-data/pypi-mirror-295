import subprocess


def main():
    conf = ["[flake8]", "ignore = E501", "exclude = venv"]
    with open(".flake8", "w", encoding="utf-8") as f:
        f.write("\n".join(conf))
    cmd_list = [
        r"venv\Scripts\activate.bat",
        "black .",
        "isort .",
        "flake8 .",
        "pytest",
    ]
    subprocess.run("&&".join(cmd_list), shell=True)
