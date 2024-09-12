import logging
import os
import re
import sys
from typing import List

from lupin_grognard.core.commit.commit import Commit
from lupin_grognard.core.config import (
    COMMIT_DELIMITER,
    INITIAL_COMMIT,
    MAIN_BRANCHES_REGEX,
    MAJOR_COMMIT_TYPES,
)
from lupin_grognard.core.git import Git


def read_file(file: str) -> str:
    with open(f"{file}", "r", encoding="utf-8") as file:
        data = file.read()
        return data


def write_file(file: str, content: str):
    with open(f"{file}", "w", encoding="utf-8") as outfile:
        outfile.write(content)


def get_version():
    """get version from setup.cfg file and
    update __version__ in lupin_grognard.__init__.py
    """
    setup_cfg = read_file("setup.cfg")
    _version = re.search(
        r"(^version = )(\d{1,2}\.\d{1,2}\.\d{1,2})(\.[a-z]{1,})?(\d{1,2})?",
        setup_cfg,
        re.MULTILINE,
    )
    version = ""
    for group in _version.group(2, 3, 4):
        if group is not None:
            version = version + str(group)
    content = f'__version__ = "{version}"\n'
    write_file(file="lupin_grognard/__init__.py", content=content)
    return version


def get_current_branch_name() -> str:
    branch_name = Git().get_branch_name()
    # branch name can be messing if running in CI
    if not branch_name:
        branch_name = os.getenv("CI_COMMIT_BRANCH")
    if not branch_name:
        branch_name = os.getenv("CI_MERGE_REQUEST_SOURCE_BRANCH_NAME")
    if not branch_name:
        return ""
    return branch_name


def display_supported_commit_types() -> None:
    commit_type = [
        "build",
        "bump",
        "ci",
        "deps(add|change|remove)",
        "docs",
        "enabler",
        "feat(add|change|remove)",
        "fixbug",
        "fixdefect(JAMA-xxx)",
        "refactor",
        "test",
    ]
    print("Supported commit types: " + ", ".join(commit_type))
    print(
        "Only one commit of a major type is allowed per merge branch: "
        f'{", ".join(MAJOR_COMMIT_TYPES[:-1])}, or {MAJOR_COMMIT_TYPES[-1]}.'
    )


def display_current_branch_name(current_branch_name: str) -> None:
    if current_branch_name:
        print(f"Current branch name is '{current_branch_name}'")
    else:
        print("Current branch name is not available")


def display_number_of_commits_to_check(commits: List[Commit]):
    number_commits_to_check = len(commits)
    if number_commits_to_check == 0:
        print("0 commit to check")
        sys.exit(0)
    elif number_commits_to_check == 1:
        print(f"Found {number_commits_to_check} commit to check:")
    else:
        print(f"Found {number_commits_to_check} commits to check:")


def generate_commit_list(commits_string: str) -> List[Commit]:
    """Geneartes the list of commits from Git().get_log().stdout value"""
    return [
        Commit(commit)
        for commit in commits_string.split(COMMIT_DELIMITER)
        if len(commit) > 0
    ]


def is_merge_commit_in_branch_list(commit: Commit) -> bool:
    """
    Check if the commit matches the pattern of a merge commit.

    Args:
        commit: Commit object

    Returns:
        True if the commit matches the pattern of a merge commit, False otherwise."""
    pattern = rf"^Merge branch '.*' into '({MAIN_BRANCHES_REGEX})'"
    return re.match(pattern, commit.title)


def generate_commits_range_to_check(
    commits: List[Commit],
    initial_commits: List[str] = INITIAL_COMMIT,
) -> List:
    """
    generates a list of message ranges starting with INITIAL_COMMIT
    or the last merge into a branch contained in the branch list

    Args:
        branch_list: list of branch names
        commits: list of Commit objects
        initial_commits: list of initial commit messages

    Returns:
        list of Commit objects to check
    """

    for index, commit in enumerate(commits):
        if commit.is_gitlab_merge_commit():
            if is_merge_commit_in_branch_list(commit):
                return commits[:index]
        elif commit.title in initial_commits:
            return commits[:index]
    return list()


def configure_logging():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO
    )
