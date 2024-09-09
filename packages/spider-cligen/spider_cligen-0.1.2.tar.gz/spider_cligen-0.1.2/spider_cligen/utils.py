import os
from spider_cligen.exceptions import PathCreateError, FileCreateError
import re
from datetime import datetime

year = datetime.now().year
PROJECT_TYPES = {
    'package',
    'web',
    'mobile',
    'desktop',
    'api',
    'scripts',
    'cli',
}

BASE_DIR = os.path.abspath('.')
SPIDERCLI_DIR = os.path.dirname(os.path.relpath(__file__))
TEMPLATES_DIR = os.path.join(SPIDERCLI_DIR,'templates')
LICENSES_DIR  = os.path.join(TEMPLATES_DIR,'licenses')
DEFAULT_CI_SERVICE = 'github'
DEFAULT_LICENSE = 'MIT'

def get_or_create_file(path,filename,data):
    file_path = os.path.join(path,filename)
    if os.path.exists(file_path):
        return file_path
    try:
        with open(file_path,'w',encoding='utf-8') as f:
            f.write(data)
        return file_path
    except FileCreateError:
        raise FileCreateError

def get_or_create_path(path_name,*args):
    path_dir = os.path.join(BASE_DIR,f'{path_name}/')
    if args:
        for arg in args:
            path_dir = os.path.join(path_dir,arg)
    
    if os.path.exists(path_dir):
        return path_dir
    else:
        try:
            os.makedirs(path_dir)
        except PathCreateError:
            raise PathCreateError

    return path_dir

def sub_string(str_to_relpace,new_str,data):
    regex = re.compile(str_to_relpace)
    new_data = regex.sub(new_str,data)
    return new_data


def generate_mit_license(project_owner):
    
    file_dir = os.path.join(LICENSES_DIR,'MIT.txt')
    data = ''
    with open(file_dir,encoding='utf-8') as f:
        data = f.read()
    data = sub_string('AUTHOR/COMPANYNAME',project_owner,data)
    data = sub_string('YEAR',f'{year}',data)
    return data

def generate_apache_license(project_owner):
    
    file_dir = os.path.join(LICENSES_DIR,'Apache.txt')
    data = ''
    with open(file_dir,encoding='utf-8') as f:
        data = f.read()
    data = sub_string('AUTHOR/COMPANYNAME',project_owner,data)
    data = sub_string('YEAR',f'{year}',data)
    return data

def generate_bsd3_license(project_owner):
    
    file_dir = os.path.join(LICENSES_DIR,'BSD3Clause.txt')
    data = ''
    with open(file_dir,encoding='utf-8') as f:
        data = f.read()
    data = sub_string('AUTHOR/COMPANYNAME',project_owner,data)
    data = sub_string('YEAR',f'{year}',data)
    return data

def generate_cco_license(project_owner):
    
    file_dir = os.path.join(LICENSES_DIR,'CCO.txt')
    data = ''
    with open(file_dir,encoding='utf-8') as f:
        data = f.read()
    data = sub_string('AUTHOR/COMPANYNAME',project_owner,data)
    data = sub_string('YEAR',f'{year}',data)
    return data

def generate_gplv3_license(project_owner):
    
    file_dir = os.path.join(LICENSES_DIR,'GPLv3.txt')
    data = ''
    with open(file_dir,encoding='utf-8') as f:
        data = f.read()
    data = sub_string('AUTHOR/COMPANYNAME',project_owner,data)
    data = sub_string('YEAR',f'{year}',data)
    return data

def generate_setupconfig(project_name,project_owner,owner_email):
    file_dir = os.path.join(TEMPLATES_DIR,'config','setup.py')
    data = ''
    with open(file_dir,encoding='utf-8') as f:
        data = f.read()
    data = sub_string('project_owner',project_owner,data)
    data = sub_string('owner_email',owner_email,data)
    data = sub_string(re.compile(r'project_name|project-name'),project_name,data)
    return data

def generate_githubaction_workflow_file():
    file_dir = os.path.join(TEMPLATES_DIR,'github','workflows','ci.yml')
    data = ''
    with open(file_dir,encoding='utf-8') as f:
        data = f.read()
    return data

def generate_gitlab_workflow_file():
    file_dir = os.path.join(TEMPLATES_DIR,'gitlab','.gitlab-ci.yml')
    data = ''
    with open(file_dir,encoding='utf-8') as f:
        data = f.read()
    return data

def generate_circleci_workflow_file():
    file_dir = os.path.join(TEMPLATES_DIR,'circleci','config.yml')
    data = ''
    with open(file_dir,encoding='utf-8') as f:
        data = f.read()
    return data

def generate_project_name(name): return '_'.join(name.split())

def generate_gitignore():
    file_dir = os.path.join(TEMPLATES_DIR,'git','.gitignore')
    data = ''
    with open(file_dir,encoding='utf-8') as f:
        data = f.read()
    return data

def generate_manifest():
    file_dir = os.path.join(TEMPLATES_DIR,'config','MANIFEST.in')
    data = ''
    with open(file_dir,encoding='utf-8') as f:
        data = f.read()
    
    return data

def generate_readme(project_name):
    file_dir = os.path.join(TEMPLATES_DIR,'README.md')
    data = ''
    with open(file_dir,encoding='utf-8') as f:
        data = f.read()
    data = sub_string('project_name',project_name,data)  
    return data

def generate_pyproject():
    file_dir = os.path.join(TEMPLATES_DIR,'config','pyproject.toml')
    data = ''
    with open(file_dir,encoding='utf-8') as f:
        data = f.read()
    return data