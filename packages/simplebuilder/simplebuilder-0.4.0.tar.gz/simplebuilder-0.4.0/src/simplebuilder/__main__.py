"""Make README more readable.

This file replaces relative path links with GitHub links and add warning in front of the long description.

Last modified at 2023-06-20; 12th edition.
"""

from __future__ import annotations

import argparse
import contextlib
import os
import re
import shutil
from pathlib import Path

import tomlkit

ProjectData = dict

cwd = Path.cwd()
pyproject_path = cwd / "pyproject.toml"

def build_parser():
    parser = argparse.ArgumentParser(
        "simplebuilder",
        "Simple build script for packages hosted on GitHub",
    )
    parser.add_argument("--preserve-dist", action="store_true", help="Don't delete `dist/` directory.")
    parser.add_argument("--branch", "--branch-name", "-B", type=str, default=None, help="Main branch name (usually `main` or `master`).")
    return parser


def load_project_data() -> ProjectData:
    return tomlkit.parse(pyproject_path.read_text())


def match_url(url: str) -> tuple[str, str]:
    result = re.match(r"(https?:\/\/)?github[.]com\/(?P<user>\w+)\/(?P<project>\w+)", url)
    if result is None:
        raise ValueError("URL is invalid or not a github URL.")
    return result["user"], result["project"]


def build_readme(github_project_url: str, project_name: str, username: str, branch_name: str) -> str:
    def make_relative_link_work(match: re.Match) -> str:
        if match.group("img"):
            return (
                f'[{match.group("description")}](https://raw.githubusercontent.com/{username}'
                f'/{project_name}/{branch_name}/{match.group("path")})'
            )

        return f'[{match.group("description")}]({github_project_url}/blob/{branch_name}/{match.group("path")})'

    long_description = f"**Check latest version [here]({github_project_url}).**\n"
    long_description += Path("README.md").read_text(encoding="utf-8")
    long_description = re.sub(
        r"(?P<img>!?)\[(?P<description>.*?)\]\(((?:\.\.\/)+|\.\/|\/)(?P<path>.*?)\)",
        make_relative_link_work,
        long_description,
    )
    return long_description


def upload_project():
    if "PYPI_TOKEN" not in os.environ:
        raise ValueError("Environment variable `PYPI_TOKEN` does not exist.")

    # Getting environment variable from `os.environ` makes this operation OS-independent.
    os.system(f'poetry publish -u __token__ -p {os.environ["PYPI_TOKEN"]}')


def get_default_branch_name():
    # very error-prone
    head_file = cwd / ".git" / "HEAD"
    content = head_file.read_text("utf-8")
    if "master" in content:
        return "master"
    if "main" in content:
        return "main"
    return None


def main(argv=None):
    # parse args
    parser = build_parser()
    args = parser.parse_args(argv)
    delete_dist = args.preserve_dist
    branch = args.branch

    # get data from pyproject
    project_data = load_project_data()
    # build_data = project_data.get("tool", {}).get("simplebuilder", {})
    name = project_data["project"]["name"]
    url = project_data["project"]["urls"]["Repository"]
    branch = branch or get_default_branch_name() or "master"

    # construct github project url
    username, project_name = match_url(url)
    github_project_url = f"https://github.com/{username}/{project_name}"

    # remove dist if exist
    if delete_dist:
        with contextlib.suppress(FileNotFoundError):
            shutil.rmtree("dist")

    long_description = build_readme(github_project_url, name, username, branch)

    readme_build = cwd / "README-build.md"
    readme_build.write_text(long_description, encoding="utf-8")


if __name__ == "__main__":
    main()
