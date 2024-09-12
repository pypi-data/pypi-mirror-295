import os

import typer

from lupin_grognard.__init__ import __version__
from lupin_grognard.core.check import (
    check_commit,
    check_max_allowed_major_commits,
    check_same_author_from_current_branch,
)
from lupin_grognard.core.commit.commit import add_additional_commit_info
from lupin_grognard.core.commit.commit_validator import (
    define_commits_check_mode,
    define_permissive_mode,
    CommitCheckModes,
)
from lupin_grognard.core.doc_generator.changelog import Changelog
from lupin_grognard.core.doc_generator.reviewlog import Reviewlog
from lupin_grognard.core.doc_generator.ros2_docs import Ros2Docs
from lupin_grognard.core.git import Git
from lupin_grognard.core.tools.ros2.package import find_ros_packages

from .core.tools.log_utils import die, info, warn
from .core.tools.utils import (
    configure_logging,
    display_current_branch_name,
    display_number_of_commits_to_check,
    display_supported_commit_types,
    generate_commit_list,
    generate_commits_range_to_check,
    get_current_branch_name,
)


cli = typer.Typer()


def tag_option() -> typer.Option:
    return typer.Option(
        None, "--from-tag", "-ft", help="Tag to start listing commits from (optional)"
    )


def output_option() -> typer.Option:
    return typer.Option(
        os.getcwd(),
        "--output",
        "-o",
        help="Directory to save the log file (default: current directory)",
    )


@cli.command()
def version():
    print(f"Version: {__version__}")


@cli.command()
def check_commits(
    CHECK_ALL_COMMITS: bool = typer.Option(
        False, "--all", "-a", help="check all commits from initial commit"
    ),
    permissive_mode: bool = typer.Option(
        False, "--permissive", "-p", help="ignore command failure"
    ),
    no_approvers: bool = typer.Option(
        False, "--no-approvers", "-na", help="ignore approver check"
    ),
    tag: str = tag_option(),
):
    """
    Supported commit types: build, bump, ci, deps(add|change|remove), docs, enabler,
    feat(add|change|remove), fixbug, fixdefect(JAMA-xxx), refactor, test.
    Only one major commit types allowed per branch: "enabler", "feat", "fixbug", fixdefect or "refactor".

    Check every commit message since the last "merge request" in any of the branches in the
    MAIN_BRANCHES_REGEX : "main|master|release/.+|feature/.+|dev|develop|development"

    - With --all option :
    grog check-commits [--all or -a] to check all commits from initial commit.
    This option is automatically set if current branch is a main one.

    - With --permissive option :
    grog check-commits [--permissive or -p] to ignore command failure.
    This option is ignored for the 'main' and 'master' branches.

    - With --no-approvers option :
    grog check-commits [--no-approvers or -na] to ignore approver check.
    """
    configure_logging()
    git = Git()
    git.ensure_valid_git_repository()

    current_branch_name = get_current_branch_name()
    check_mode = define_commits_check_mode(
        current_branch=current_branch_name,
        CHECK_ALL_COMMITS_flag=CHECK_ALL_COMMITS,
    )

    permissive_mode = define_permissive_mode(
        check_mode=check_mode,
        permissive_mode=permissive_mode,
    )

    if CHECK_ALL_COMMITS:
        info(msg="Processing all commits since initial commit as '--all' option is set")
        git.ensure_not_shallow_clone()
    if no_approvers:
        warn(msg="Approver check disabled as '--no-approvers' option is set")

    if check_mode == CommitCheckModes.CHECK_ALL_COMMITS:
        git_log = git.get_log(tag=tag)
        commits = generate_commit_list(git_log.stdout)

    elif check_mode == CommitCheckModes.CHECK_CURRENT_BRANCH_ONLY:
        git_log = git.get_log(max_line_count=50, first_parent=True)
        commits = generate_commit_list(git_log.stdout)
        commits = generate_commits_range_to_check(
            commits=commits,
        )

    if check_max_allowed_major_commits(commits=commits, all_option=CHECK_ALL_COMMITS):
        display_supported_commit_types()
        display_current_branch_name(current_branch_name=current_branch_name)
        display_number_of_commits_to_check(commits=commits)

        if check_mode == CommitCheckModes.CHECK_CURRENT_BRANCH_ONLY:
            check_same_author_from_current_branch(commits=commits)

        check_commit(
            commits=commits,
            check_mode=check_mode,
            permissive_mode=permissive_mode,
            no_approvers=no_approvers,
        )


@cli.command()
def changelog(output: str = output_option(), tag: str = tag_option()):
    """Generate changelog
    Run this command `grog changelog` from a git repository to generate changelog.md file in the current directory.

    - With --output option :
    grog changelog [--output or -o] {string} to set the output to create changelog file.

    - With --from-tag option :
    grog changelog [--from-tag or -ft] {string} to set the tag to start listing commits from.
    """
    configure_logging()
    git = Git()
    git.ensure_valid_git_repository()
    git_log = git.get_log(tag=tag)
    if git_log.stderr:
        die(f"git error {git_log.return_code}, {git_log.stderr}")
    commits = generate_commit_list(commits_string=git_log.stdout)
    commits = add_additional_commit_info(commits=commits)
    Changelog(commits=commits).generate(output)


@cli.command()
def reviewlog(output: str = output_option(), tag: str = tag_option()):
    """Generate REVIEWLOG.html
    Run this command `grog reviewlog` from a git repository to generate REVIEWLOG.html file in the current directory.

    - With --output option :
    grog reviewlog [--output or -o] {string} to set the output to create reviewlog file.

    - With --from-tag option :
    grog changelog [--from-tag or -ft] {string} to set the tag to start listing commits from.
    """
    configure_logging()
    git = Git()
    git.ensure_valid_git_repository()
    git_log = git.get_log(tag=tag)
    if git_log.stderr:
        die(f"git error {git_log.return_code}, {git_log.stderr}")
    commits = generate_commit_list(commits_string=git_log.stdout)
    commits = add_additional_commit_info(commits=commits)
    Reviewlog(commits=commits).generate(output)


@cli.command()
def ros2docs(
    path: str = typer.Option(
        ..., "--path", "-p", help="path to search for ROS2 packages"
    )
):
    """Generate ROS2 documentation"""
    configure_logging()

    ros_packages = find_ros_packages(path)
    for path in ros_packages:
        api_doc = Ros2Docs(path=path)
        api_doc.generate_api_docs()
