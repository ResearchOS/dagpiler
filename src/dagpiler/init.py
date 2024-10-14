import os
import requests
import toml, yaml

# GitHub repository details
OWNER = "mtillman14"
REPO = "dagpiler"
BRANCH = "main"  # or the branch you want to replicate

INIT_TEMPLATE_DIR = "init_template_directory"

def init_package():
    """Download the init_template_directory from the package's GitHub repository."""
    # GitHub API URL to fetch repository content
    api_url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees/{BRANCH}?recursive=1"
    local_path = os.getcwd()
    # Fetch the repository structure
    response = requests.get(api_url)
    if response.status_code != 200:
        print("Failed to fetch repository structure:", response.status_code, response.text)
        return
    tree = response.json().get('tree', [])
    for item in tree:
        if INIT_TEMPLATE_DIR not in item['path']:
            continue
        # Process directories
        item_path = os.path.join(local_path, item['path'])
        if item['type'] == 'tree':
            os.makedirs(item_path, exist_ok=True)
        # Process files
        elif item['type'] == 'blob':
            # Create directories as needed and download the file
            os.makedirs(os.path.dirname(item_path), exist_ok=True)
            file_url = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/{item['path']}"
            download_file(file_url, item_path)
    print("Project initialized! Personalizing, please answer the following questions:")
    project_name = input("Project name: ")
    if not project_name:
        raise ValueError("Project name is required!")
    author_name = input("Author name (Enter to skip): ")
    author_email = input("Author email (Enter to skip): ")
    pyproject_toml_path = os.path.join(local_path, "pyproject.toml")
    personalize_pyproject_toml(pyproject_toml_path, project_name, author_name, author_email)    
    # Change src/project_name to src/<project_name>
    os.rename(os.path.join(local_path, "src", "project_name"), os.path.join(local_path, "src", project_name))
    # Update the metadata in mkdocs.yml
    yml_path = os.path.join(local_path, INIT_TEMPLATE_DIR, "mkdocs.yml")
    personalize_mkdocs_yml(yml_path, project_name)      
    os.system("pip install -e .")
    print("Project initialized successfully!")    

def personalize_mkdocs_yml(yml_path: str, project_name: str, author_name: str):
    with open(yml_path, "r") as file:
        mkdocs_yml = yaml.safe_load(file)  
    mkdocs_yml["site_name"] = project_name
    if author_name:
        mkdocs_yml["site_author"] = author_name
    with open(yml_path, "w") as file:
        yaml.dump(mkdocs_yml, file)
    print("Project name updated in mkdocs.yml")

def personalize_pyproject_toml(toml_path: str, project_name: str, author_name: str, author_email: str):
    with open(toml_path, "r") as file:
        pyproject_toml = toml.load(file)
    pyproject_toml["project"]["name"] = project_name
    if author_name:
        pyproject_toml["authors"]["name"] = author_name
    if author_email:
        pyproject_toml["authors"]["email"] = author_email
    with open(toml_path, "w") as file:
        toml.dump(pyproject_toml, file)
    print("Project name updated in pyproject.toml")

# Function to download a file
def download_file(file_url, save_path):
    file_response = requests.get(file_url)
    if file_response.status_code != 200:
        print(f"Failed to download {file_url}: {file_response.status_code}")
        return
    if os.path.exists(save_path):
        print(f"File already exists: {save_path}")
        return
    with open(save_path, "wb") as file:
        file.write(file_response.content)


