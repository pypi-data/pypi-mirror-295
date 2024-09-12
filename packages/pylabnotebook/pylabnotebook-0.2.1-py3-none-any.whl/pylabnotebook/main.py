"""PYLABNOTEBOOK
This module is the main module where all the functions to run the cli of pylabnotebook are defined.
"""
import argparse
import os
from datetime import datetime
import subprocess
import json
import shutil
import sys
import re
from typing import Union
from .version import __version__

# Useful values
YELLOW: str = '\033[0;33m'
GREEN: str = '\033[0;32m'
NCOL: str = '\033[0m'
RED: str = '\033[0;31m'

def create_labnotebook(name: str) -> None:
    """Create new labnotebook.

    This function creates a new labnotebook by creating a new .labnotebook folder with all the 
    necessary files included.

    :param name: Name of the project.
    :type name: str
    """

    # 1. Check if .git folder is present
    if not os.path.exists(".git"):
        print("Error: There is no .git folder in the current working directory.")
        print("Please go to the folder where .git is to create a new notebook in the same folder or run 'git init'.") # pylint: disable=line-too-long
        return

    # 2. Create .labnotebook directory if it doesn't exist, otherwise return an error
    try:
        os.makedirs(".labnotebook")
    except OSError:
        print(".labnotebook folder is already present. If you want to create a new .labnotebook directory, you have to firstly delete it.") # pylint: disable=line-too-long
        return

    # 3. Get useful variables
    today: str = datetime.now().strftime('%Y-%m-%d')
    aut: str = subprocess.check_output(["git", "config", "--get", "user.name"],
                                       universal_newlines = True).strip()

    # 4. Create config file
    create_config_json(name = name, aut = aut)

    # 5. Create HEAD, BODY and FOOTER
    create_head_html(name = name)
    create_body_html(name, today, aut)
    script_dir: str = os.path.dirname(os.path.abspath(__file__))
    footer_template_path: str = os.path.join(script_dir, "templates", "footer.html")
    new_footer_path: str = os.path.join(".labnotebook", "footer.html")
    shutil.copy(footer_template_path, new_footer_path)

    # 6. Copy style.css file
    css_template_path: str = os.path.join(script_dir, "templates", "style.css")
    new_css_path: str = os.path.join(".labnotebook", "labstyles.css")
    shutil.copy(css_template_path, new_css_path)

    # 7. Return messages
    print(f"\n{GREEN}.labnotebook folder successfully created")
    print(f"{YELLOW}Mandatory: when updating the notebook, make sure you are in {os.getcwd()}")
    print("Never change the .labnotebook folder name or content")
    print(NCOL)


def create_config_json(name: str, aut: str) -> None:
    """Create configuration file.

    This function creates the config.json file of the notebook inside .labnotebook folder.

    :param name: Name of the notebook.
    :type name: str
    :param aut: Author of the notebook.
    :type aut: str
    """
    config: dict = {"NOTEBOOK_NAME": f"{name}",
                    "LAB_AUTHOR": f"{aut}",
                    "LAST_COMMIT": None,
                    "LAST_DAY": None,
                    "SHOW_ANALYSIS_FILES": True,
                    "LAB_CSS": ".labnotebook/labstyles.css",
                    "ANALYSIS_EXT": ['.html']}

    filename: str = '.labnotebook/config.json'
    with open(filename, 'w', encoding = 'utf8') as file:
        json.dump(config, file, indent = 4)


def create_head_html(name: str) -> None:
    """Create head html file.

    This function creates the head.html file based on the head template, by changing the title meta.

    :param name: Name of the notebook (or project). This will be added as part of the title tag in
    head.
    :type name: str
    """
    # 1. Get the directory where the current script is located
    script_dir: str = os.path.dirname(os.path.abspath(__file__))

    # 2. Define the path to the 'templates' folder relative to the script's directory
    head_template_path: str = os.path.join(script_dir, "templates", "head.html")

    # 3. Perform the substitution
    try:
        # 3.1 Read the content of the template file
        with open(head_template_path, "r", encoding = 'utf8') as template_file:
            template_content: str = template_file.read()

        # 3.2 Perform the substitution
        head_content: str = template_content.replace("{name_placeholder}", name)

        # 3.3 Define the path for the new .labnotebook/head.html file
        new_head_path: str = os.path.join(".labnotebook", "head.html")

        # 3.4 Write the modified content to the new file
        with open(new_head_path, "w", encoding = 'utf8') as new_head_file:
            new_head_file.write(head_content)

    except FileNotFoundError:
        print("Template file not found.")


def create_body_html(name: str, today: str, aut: str) -> None:
    """Create body html file.

    This function creates the body.html file based on the body template, by changing the title, 
    the author and the creation date.

    :param name:  Name of the notebook (or project). This will be displayed has h1 in the body.
    :type name: str
    :param today: date of creation. This will be shown alongside "Created on:" in the top of the
    body.
    :type today: str
    :param aut: author of the notebook. This will be shown alongside "Author:" in the top of the
    body
    :type aut: str
    """
    # 1. Get the directory where the current script is located
    script_dir: str = os.path.dirname(os.path.abspath(__file__))

    # 2. Define the path to the 'templates' folder relative to the script's directory
    body_template_path: str = os.path.join(script_dir, "templates", "body.html")

    # 3. Perform the substitution
    try:
        # 3.1 Read the content of the template file
        with open(body_template_path, "r", encoding = 'utf8') as template_file:
            template_content: str = template_file.read()

        # 3.2 Perform the substitution
        body_content: str = (template_content.replace("{name_placeholder}", name).
                             replace("{today_placeholder}", today).
                             replace("{aut_placeholder}", aut))

        # 3.3 Define the path for the new .labnotebook/head.html file
        new_body_path: str = os.path.join(".labnotebook", "body.html")

        # 3.4 Write the modified content to the new file
        with open(new_body_path, "w", encoding = 'utf8') as new_body_file:
            new_body_file.write(body_content)

    except FileNotFoundError:
        print("Template file not found.")


def update_labnotebook(force_update: bool) -> None:
    """Update labnotebook files.

    This function updates body.html and config.json files in .labonotebook folder by looping through 
    all commits not already inclded.

    :param force_update: whether to force the update by starting from the beginning of the commit history. Mandatory if last commit in config.json is no more present in commit history (e.g. rebase, reset or any change in commit history) # pylint: disable=line-too-long
    :type force_update: bool

    """

    # 2. Check for .labnotebook folder and config.json files
    if not os.path.exists(".labnotebook"):
        print(f"{RED}Error: There is no .labnotebook folder in the current working directory. "
              "Please go to the folder where .labnotebook is.")
        sys.exit(2)

    config_file_path: str = os.path.join(".labnotebook", "config.json")
    try:
        with open(config_file_path, "r", encoding = 'utf8') as config_file:
            config: dict = json.load(config_file)
    except FileNotFoundError:
        print(f"{RED}Error: There is no config file in .labnotebook folder. Please provide the config file.") # pylint: disable=line-too-long
        sys.exit(2)

    # 3. Check for staged files
    git_status: str = subprocess.run("git status", shell = True, stdout = subprocess.PIPE,
                                text = True, check = False)
    if "Changes to be committed:" in git_status.stdout:
        print(f"{RED}Error: You have staged files to be committed. This is incompatible with updatenotebook. " # pylint: disable=line-too-long
              "Please commit those changes, restore the files, or stage them prior to running this function.") # pylint: disable=line-too-long
        sys.exit(1)

    # 4. Reset config and head if force_update
    if force_update:
        create_config_json(name = config.get('NOTEBOOK_NAME'),
                           aut = config.get('LAB_AUTHOR'))
        with open(config_file_path, "r", encoding = 'utf8') as config_file:
            config: dict = json.load(config_file)
        create_body_html(name = config.get('NOTEBOOK_NAME'),
                         today = datetime.now().strftime('%Y-%m-%d'),
                         aut = config.get('LAB_AUTHOR'))

    # 5. Get list of commits sha
    last_commit: str = config.get('LAST_COMMIT')
    sha_list: list[str] = get_sha_list(last_commit)

    # 6. Remove main and body closing tags from body.html
    with open(".labnotebook/body.html", "r", encoding = 'utf8') as body_file:
        body_content: str = body_file.read()
        body_content: str = (body_content.replace("</main>", "").
                             replace("</body>", ""))

    # 7. Get info about each commit
    analysis_ext: list[str] = config.get('ANALYSIS_EXT')
    excluded_patterns: list[str] = get_excluded_patterns()
    commits_info: dict = {sha: get_commit_info(sha, analysis_ext, excluded_patterns) for sha
                          in sha_list}

    # 8. Write info into body.html and update config
    write_update_files(commits_info, body_content, config)

    # 9. Commit changes in .labnotebook folder
    commit_labnotebook()


def get_sha_list(last_commit: Union[str, None]) -> list[str]:
    """Get sha list since last commit in notebook

    This functions returns a list of commits sha (from oldest to newest) that have not been already 
    included in the notebook.

    :param last_commit: sha of the last commit in the notebook.
    :type last_commit: str or None
    :return: list of the commits not included in the notebook since last_commit.
    :rtype: list[str]
    """

    # 1. Get list of all commits
    git_sha: list[str] = subprocess.run("git log --pretty=format:%h --reverse", shell = True,
                                        stdout = subprocess.PIPE, text = True, check = False).stdout.split('\n') # pylint: disable=line-too-long

    # 2. Subset for new commits
    # 2.1 If git history is empty, return error
    if git_sha == ['']:
        print(f"{RED}Error: Git history is empty")
        sys.exit(5)

    # 2.2 Return all if last commit is None
    if last_commit is None:
        return git_sha

    # 2.3 Raise error if last commit is not in git_sha list
    if last_commit not in git_sha:
        print(f"{RED}Error: Last commit used for the lab notebook ({last_commit}) is not in the current git log history." # pylint: disable=line-too-long
              f"\nIt is possible that you have changed commit history. Please check your git log and insert the commit SHA to use in the config file or force the update to start again from the beginning of the git history using labnotebook update -f/--force.") # pylint: disable=line-too-long
        sys.exit(5)

    # 2.4 Perform the subset
    index: int = git_sha.index(last_commit)
    git_sha: str = git_sha[index + 1:]

    # 2.5 Interrupt if last_commit is actually the last commit in history
    if len(git_sha) == 0:
        print(f"{YELLOW}Warning: LAST_COMMIT is already the last commit in history. Nothing to update.") # pylint: disable=line-too-long
        sys.exit(5)

    # 3. Return git_sha
    return git_sha


def get_excluded_patterns() -> list[str]:
    """Get the exluded patterns for analysis files.

    This functions returns a list of the patterns to exclude in analysis files. It reads the 
    .labignore file in root directory, if exists.

    :return: list of excluded patterns.
    :rtype: list[str]
    """
    try:
        with open('.labignore', 'r', encoding = 'utf8') as f:
            excluded_patterns: list[str] = f.read().splitlines()
            excluded_patterns: list[str] = [pattern.replace('*', '.*') for pattern
                                            in excluded_patterns]
    except FileNotFoundError:
        excluded_patterns: list = []

    return excluded_patterns



def get_commit_info(commit_sha: str, analysis_ext: list[str], excluded_patterns: list[str]) -> dict:
    """Get commit info.

    This function returns a dictionary of the information about the commit specified in commit_sha. 
    These info are: date, author, title, message, changed files and analysis_files (based on both
    analysis_ext and excluded_patterns).

    :param commit_sha: sha of the commit of interest.
    :type commit_sha: str
    :param analysis_ext: list of the file extensions used as reference for analysis files.
    :type analysis_ext: list[str]
    :param excluded_patterns: list of the pattern to be excluded from the analysis files.
    :type excluded_patterns: list[str]
    
    :return: information about the commit specified in commit_sha: date, author, title, message, 
    changed files and analysis_files (based on both analysis_ext and excluded_patterns).
    :rtype: dict
    """
    date, author, title = subprocess.check_output(['git', 'log', '-n', '1', '--pretty=format:%cs%n%an%n%s', commit_sha], text = True).strip().split('\n') # pylint: disable=line-too-long
    message: str = subprocess.check_output(['git', 'log', '-n', '1', '--pretty=format:%b', commit_sha], text=True).strip() # pylint: disable=line-too-long
    pattern: str = r"(\.|:|!|\?)\n"
    replacement: str = r"\1<br>\n"
    message = re.sub(pattern, replacement, message).replace('\n\n', '\n<br>\n')
    changed_files: str = subprocess.check_output(['git', 'show', '--pretty=%n', '--name-status', commit_sha], text=True).strip().split('\n') # pylint: disable=line-too-long
    changed_files: dict = {file.split('\t')[1] : file.split('\t')[0] for file in changed_files}
    analysis_files: list[str] = [key for key, _ in changed_files.items()
                                 if any(ext in key for ext in analysis_ext) and
                                 os.path.isfile(key) and not
                                 any(re.search(pattern, key) for pattern in excluded_patterns)]
    commit_info: dict = {'date': date,
                         'author': author,
                         'title': title,
                         'message': message,
                         'changed_files': changed_files,
                         'analysis_files': analysis_files}

    return commit_info


def write_update_files(commits_info: dict, body_content: str, config: dict) -> None:
    """Write commits update in body.html.

    This function writes the commit elements into body.html and updates the config.json file.

    :param commits_info: dictionary with the info about the new commits to write in body.html.
    :type commits_info: dict
    :param body_content: content of the actual body.html.
    :type body_content: str
    :param config: configuration dictionary. This will be updated and saved in config.json.
    :type config: dict
    """
    # 1. Loop through commits
    for sha, commit in commits_info.items():

        # 1.1 Check if labnotebook commit and ignore it
        if commit.get('author') == "labnotebook":
            continue

        # 1.1 Check last day
        if config.get('LAST_DAY') != commit.get('date'):
            body_content += f"<h2 class='day-el'>{commit.get('date')}</h2>\n\n"
            config['LAST_DAY'] = commit.get('date')

        # 1.2 Write commit div
        body_content += f"<div class='commit-el' id='{sha}'>\n"
        body_content += f"<h3 class='title-el'>{commit.get('title')}</h3>\n"
        if commit.get('message') == '':
            pass
        else:
            body_content += f"<p class='mess-el'>{commit.get('message')}</p>\n"
        body_content += f"<p class='author-el'>Author: {commit.get('author')}</p>\n"
        body_content += f"<p class='sha-el'>sha: {sha}</p>\n"
        if len(commit.get('analysis_files')) == 0:
            body_content += "<div class='analyses-el'>Analysis file/s: <code>none</code></div>\n"
        else:
            body_content += "<div class='analyses-el'>Analysis file/s:\n<ul class='analysis_list'>\n" # pylint: disable=line-too-long
            for a_file in commit.get('analysis_files'):
                body_content += f"<li><code><a href='{a_file}' target='_blank'>{a_file}</a></code></li>\n" # pylint: disable=line-too-long
            body_content += "</ul>\n</div>\n"
        body_content += "<details>\n<summary>Changed files</summary>\n<ul class='changed_list'>\n"
        for c_file in commit.get('changed_files'):
            body_content += f"<li>{c_file}</li>\n"
        body_content += "</ul>\n</details>\n</div>\n"

        # 1.3 Update last commit
        config['LAST_COMMIT'] = f"{sha}"

    # 2. Insert closing tags
    body_content += "</main>\n</body>"

    # 3. Write body.html
    with open('.labnotebook/body.html', "w", encoding = 'utf8') as new_body_file:
        new_body_file.write(body_content)

    # 4. Write config.json
    with open(".labnotebook/config.json", 'w', encoding = 'utf8') as file:
        json.dump(config, file, indent = 4)


def export_labnotebook(output_file: str, force: bool, link: bool) -> None:
    """Export labnotebook to html.

    This function exports the labnotebook into a single html file ready to read and share.

    :param output_file: path of the file to create
    :type output_file: str
    :param force: whether to force the overwriting of output_file if exists.
    :type force: bool
    :param link: whether to create links to analysis files in analysis files bullet list. These links can be used to open the analysis files directly from the notebook. # pylint: disable=line-too-long
    :type link: bool

    """

    # 2. Check for .labnotebook folder, config.json and .html files
    if not os.path.exists(".labnotebook"):
        print(f"{RED}Error: There is no .labnotebook folder in the current working directory. "
              "Please go to the folder where .labnotebook is.")
        sys.exit(2)

    config_file: str = os.path.join(".labnotebook", "config.json")
    try:
        with open(config_file, "r", encoding = 'utf8') as config_file:
            config: dict = json.load(config_file)
    except FileNotFoundError:
        print(f"{RED}Error: There is no config file in .labnotebook folder. Please provide the config file.") # pylint: disable=line-too-long
        sys.exit(2)

    required_files: list[str] = [
        '.labnotebook/head.html', 
        '.labnotebook/body.html', 
        '.labnotebook/footer.html', 
        config.get('LAB_CSS')
    ]

    for file in required_files:
        if not os.path.exists(file):
            print(f"Error: There is no {file} file.")
            sys.exit(2)

    # 3. Check if file already exists and force is False
    if os.path.exists(output_file) and not force:
        print(f"{RED}Error: {output_file} already exists. Use -f/--force to overwrite it.")
        sys.exit(1)

    # 4. Read head.html and edit it
    with open('.labnotebook/head.html', 'r', encoding = 'utf8') as head_file:
        output_content: str = head_file.read()
    output_content: str = output_content.replace("</head>", "")
    if link:
        output_content += f"<link rel='stylesheet' href='{config.get('LAB_CSS')}'>\n"
    else:
        with open(config.get('LAB_CSS'), 'r', encoding = 'utf8') as style_file:
            output_content += f"<style>\n{style_file.read()}\n</style>\n"

    if not config.get('SHOW_ANALYSIS_FILES'):
        output_content += "<style>\n.analyses-el {display: none;}\n</style>\n"

    output_content += "</head>\n"

    # 5. Read body.html and insert into output content
    with open('.labnotebook/body.html', 'r', encoding = 'utf8') as body_file:
        output_content += f"{body_file.read()}\n"

    # 5. Read footer.html and insert into output content
    with open('.labnotebook/footer.html', 'r', encoding = 'utf8') as footer_file:
        output_content += f"{footer_file.read()}\n"

    # 6. Write output file
    with open(output_file, 'w', encoding = 'utf8') as of:
        of.write(output_content)

def commit_labnotebook() -> None:
    """Commit .labnotebook folder changes.

    This function adds and commits changes in .labnotebook folder by using 'labnotebook' as author
    and 'labnotebook@email.com' as email.
    """

    subprocess.run('git add .labnotebook >/dev/null', #pylint: disable=line-too-long
                   shell = True,
                   stdout = subprocess.PIPE, text = True, check = False)

    subprocess.run('GIT_COMMITTER_NAME="labnotebook" GIT_COMMITTER_EMAIL="labnotebook@email.com" git commit --author="labnotebook <labnotebook@email.com>" -m "update notebook" >/dev/null', #pylint: disable=line-too-long
                   shell = True,
                   stdout = subprocess.PIPE, text = True, check = False)


def main():
    """Main cli function handler.

    This function is the main function of the module, which handles command line input values to run
    the different functions of the labnotebook.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Lab Notebook Tool")
    parser.add_argument('--version', action = 'version', version = '%(prog)s ' + __version__,
                        help = "Show package version")

    subparsers: argparse._SubParsersAction = parser.add_subparsers(dest = "command")

    create_parser: argparse.ArgumentParser = subparsers.add_parser("create",
                                                                   help = "Create a new lab notebook") # pylint: disable=line-too-long
    create_parser.add_argument("-n", "--name", required = True,
                               help="Name of the lab notebook. If the name should contain more words, wrap them into quotes") # pylint: disable=line-too-long

    update_parser: argparse.ArgumentParser = subparsers.add_parser("update",
                                                                   help = "Update lab notebook")
    update_parser.add_argument("-f", "--force", help = "Force the update",
                               default = False, action = "store_true")

    export_parser: argparse.ArgumentParser = subparsers.add_parser("export", help = "Export lab notebook to an html file") # pylint: disable=line-too-long
    export_parser.add_argument("-o", "--output", required = True,
                               help = "Path/name of the output HTML file")
    export_parser.add_argument("-f", "--force",
                               help = "Force the overwriting of the output file if already present",
                               default = False, action = "store_true")
    export_parser.add_argument("-l", "--link", default = False, action = "store_true",
                               help = "Link style file in head. By default style file is copied in <style></style> tags in head") # pylint: disable=line-too-long

    subparsers.add_parser("commit",
                          help = "Add and commit changes in .labnotebook folder using labnotebook as author") # pylint: disable=line-too-long

    args = parser.parse_args()

    if args.command == "create":
        if not args.name:
            create_parser.error("-n/--name is required for the 'create' command. Please provide the name of the notebook.") # pylint: disable=line-too-long
        create_labnotebook(args.name)
    elif args.command == "update":
        update_labnotebook(args.force)
    elif args.command == "export":
        if not args.output:
            export_parser.error("-o/--output is required for the 'export' command. Please provide the name of the output file.") # pylint: disable=line-too-long
        export_labnotebook(args.output, args.force, args.link)
    elif args.command == "commit":
        commit_labnotebook()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
