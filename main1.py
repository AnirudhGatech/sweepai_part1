import os
from os import path
from github import Github
import evadb



import openai


openai.api_key = "your_openai_api_key"


def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=50,  
        n = 1  # You can change the number of responses you want
    )
    return response.choices[0].text.strip()

def print_red(text):
    print("\033[91m {}\033[00m".format(text))

def print_yellow(text):
    print("\033[93m {}\033[00m".format(text))

def print_green(text):
    print("\033[92m {}\033[00m".format(text))


github_token = "your_github_token"
organization_name = "your_organization"
github = Github(github_token)
organization = github.get_organization(organization_name)


connection = evadb.connection()
cursor = connection.cursor()
cursor.query(''
    CREATE TABLE IF NOT EXISTS repositories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        repository_name TEXT,
        base_branch TEXT,
        changes_executed BOOLEAN
    )
'')


repositories_to_base = {
    'first_repo': 'master',
    'second_repo': 'develop',
    'third_repo': 'master'
}


ticket = "ticket_id"
branch = f"{ticket}-update-cocoapods"


def insert_repository(repository_name, base_branch):
    cursor.query('''
        INSERT INTO repositories (repository_name, base_branch, changes_executed)
        VALUES (?, ?, ?)
    ''', (repository_name, base_branch, 0))

def update_changes_executed(repository_name):
    cursor.query('''
        UPDATE repositories
        SET changes_executed = 1
        WHERE repository_name = ?
    ''', (repository_name,))


def execute_changes(repository_name, code_change, code_description):
    print_yellow(f"Making code changes in {repository_name}")
    if not path.exists('Podfile'):
        print_red(f"Repository {repository_name} does not contain Podfile. Skipping...")
        return False

  
    code_modification = chat_with_gpt(f"Modify the following code:\n{code_change}\nDescription: {code_description}\n")
    
    
    with open('file_to_modify.txt', 'a') as file:
        file.write(code_modification)

    return True

def get_commit_title():
    cocoapods_version = os.popen('pod --version').read()
    return f"Update cocoapods to {cocoapods_version}"


def get_repository(repository_name):
    return organization.get_repo(repository_name)

def get_base_branch(repository_name):
    return repositories_to_base.get(repository_name)

def clone_repository(repository_name):
    print_yellow(f"Clone repository {repository_name}")
    repository = get_repository(repository_name)
    ssh_url = repository.ssh_url
    os.system(f"git clone {ssh_url}")

def prepare_branch(repository_name, base_branch, branch):
    print_yellow(f"Preparing branch {branch}")
    os.system(f"git add --all; git reset --hard head; git checkout {base_branch}; git pull origin {base_branch}; git checkout -b {branch}")

def is_anything_to_commit():
    if os.popen('git diff --exit-code').read():
        return True
    print_red("No changes appeared after execution. Skipping...")
    return False

def commit_and_push(branch):
    print_yellow("Commit and push")
    commit_title = get_commit_title()
    os.system('git add --all')
    os.system(f'git commit -m"{commit_title}";')
    os.system(f'git push origin {branch}')

def create_pr(branch, base_branch):
    print_yellow("Creating PR")
    pr_title = get_commit_title()
    how_to_test = "Run pod install and make sure no changes appeared"
    pr_body = f'''
    Ticket: {ticket}

    ### What has been done?
    1. {pr_title}

    ### How to test?
    1. {how_to_test}
    '''

    get_repository(repository_name).create_pull(pr_title, pr_body, base_branch, branch)

    
    print_green('\n\n\nPR successfully created 🎉')
    print(f'\nPR title: {pr_title}')
    print(f'\nPR body: {pr_body}')
    changes = os.popen('git show head').read()
    print(f'\nPR changes:\n{changes}\n')

def cleanup(repository_name):
    print_yellow("Cleanup")
    os.chdir('..')
    os.system(f'rm -rf {repository_name}')


for repository_name in repositories_to_base.keys():
    print_yellow(f"\n\n\n************************* Repository: {repository_name} *************************\n\n")
    base_branch = repositories_to_base.get(repository_name)

    
    cursor.query('SELECT changes_executed FROM repositories WHERE repository_name = ?', (repository_name,))
    row = cursor.fetchone()

    if row is not None and row[0]:
        print_yellow(f"Repository {repository_name} already processed. Skipping...")
        continue

    insert_repository(repository_name, base_branch)
    clone_repository(repository_name)
    os.chdir(repository_name)
    prepare_branch(repository_name, base_branch, branch)

    
    code_change = 'var x = 5;'
    code_description = 'Change the variable value'
    are_changes_executed = execute_changes(repository_name, code_change, code_description)

    if not are_changes_executed:
        cleanup(repository_name)
        continue

    if not is_anything_to_commit():
        cleanup(repository_name)
        continue

    commit_and_push(branch)
    create_pr(branch, base_branch)
    update_changes_executed(repository_name)
    cleanup(repository_name)
