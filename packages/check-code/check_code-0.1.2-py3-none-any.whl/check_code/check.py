import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser(description="check code")
    parser.add_argument("-a", "--all", action="store_true", help="add pytest")
    conf = ["[flake8]", "ignore = E501", "exclude = venv"]
    with open(".flake8", "w", encoding="utf-8") as f:
        f.write("\n".join(conf))
    cmd_list = [
        r"venv\Scripts\activate.bat",
        "black .",
        "isort .",
        "flake8 .",
    ]
    args = parser.parse_args()
    if args.all:
        cmd_list.append("pytest")
    subprocess.run("&&".join(cmd_list), shell=True)
