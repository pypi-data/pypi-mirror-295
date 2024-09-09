from spider_cligen.utils import PROJECT_TYPES,DEFAULT_CI_SERVICE
from spider_cligen.exceptions import(
    ProjectTypeNotExitsError,
    ContinousIntegrationServiceError,
    VenvCreateError,
    RequirementsInstallationError,
    CreateProjectStructureError
    )
import os
import subprocess
from spider_cligen.utils import (
    get_or_create_file,
    get_or_create_path,
    generate_mit_license,
    generate_apache_license,
    generate_bsd3_license,
    generate_cco_license,
    generate_gplv3_license,
    generate_setupconfig,
    generate_githubaction_workflow_file,
    generate_circleci_workflow_file,
    generate_gitlab_workflow_file,
    generate_project_name,
    generate_gitignore,
    generate_manifest,
    generate_readme,
    generate_pyproject
    )

def create_project_structure(project_type,project_name,license_type,project_owner,owner_email,ci_service):
    try:
        if project_type.lower() not in PROJECT_TYPES:
            raise ProjectTypeNotExitsError
        project_name = generate_project_name(project_name)
        project_base_dir = get_or_create_path(project_name)
        src_path = get_or_create_path(project_base_dir,'src')
        project_src_dir = get_or_create_path(src_path,project_name)
        get_or_create_file(project_src_dir,'__init__.py','')
        create_tests_path(project_base_dir)
        tests_path = get_or_create_path('tests')
        get_or_create_file(tests_path,'__init__.py','')
        create_docs_path(project_base_dir)
        create_workflows_path(project_base_dir,ci_service)
        create_readme(project_base_dir,project_name)
        create_gitignore(project_base_dir)
        create_lincense(project_base_dir,license_type,project_owner)
        create_env_file(project_base_dir)
        if project_type == 'package':
            create_manifest(project_base_dir)
            create_setupconfig(project_base_dir,project_name,project_owner,owner_email)
            create_pyproject_file(project_base_dir)
        create_venv(project_base_dir)
        if create_requirements(project_base_dir)[0]:
            install_requirements(project_base_dir)
        return project_base_dir
    except : raise CreateProjectStructureError
    
def create_readme(path,project_name):
    data = generate_readme(project_name)
    return get_or_create_file(path,'README.md',data)

def create_requirements(path):
    data = '\n'.join(input('Provide requires pakages:').split())
    file = get_or_create_file(path,'requirements.txt',data)
    if data.strip() == '':
        return [None,file]
    return [file]

def create_gitignore(path):
    data = generate_gitignore()
    return get_or_create_file(path,'.gitignore',data)

def create_lincense(path,license_type,project_owner=None):
    licenses = {
    'mit':generate_mit_license(project_owner),
    'gplv3':generate_gplv3_license(project_owner),
    'apache':generate_apache_license(project_owner),
    'bsd_3_clause':generate_bsd3_license(project_owner),
    'cco':generate_cco_license(project_owner),
    }
    data = licenses[license_type.lower()]
    return get_or_create_file(path,'LICENSE',data)

def create_manifest(path):
    data = generate_manifest()
    return get_or_create_file(path,'MANIFEST.in',data)

def create_setupconfig(path,project_name,project_owner,owner_email):
    data = generate_setupconfig(project_name,project_owner,owner_email)
    return get_or_create_file(path,'setup.py',data)

def create_tests_path(project_path):
    return get_or_create_path(project_path,'tests')

def create_docs_path(project_path):
    return get_or_create_path(project_path,'docs')

def create_workflows_path(project_path,service=DEFAULT_CI_SERVICE):
    services = {
        'github':
            {'dir':'.github/workflows/',
             'files':{
                 'ci.yml':generate_githubaction_workflow_file()
              }
        },
        'gitlab':{
            'dir':'gitlab/',
            'files':{
                '.gitlab-ci.yml':generate_gitlab_workflow_file()
            }
        },
        'circleci':{
            'dir':'circleci/',
            'files':{
                'config.yml':generate_circleci_workflow_file()
                }
        }

    }
    
    if service not in services:
        raise ContinousIntegrationServiceError
    service_path = services.get(service).get('dir')
    service_files = services.get(service).get('files')
    workflows_path = get_or_create_path(project_path,service_path)
    for filename, data in service_files.items():
        file_dir = os.path.join(project_path,service_path)
        get_or_create_file(file_dir,filename,data)
    return workflows_path

def create_env_file(path):
    return get_or_create_file(path,'.env','')

def create_venv(path):
    venv_dir = os.path.join(path,'venv')
    print('Creating virtual enviroment...')
    try:
        process = subprocess.run(['py','-m','venv',venv_dir])
        if process:
            print('Virtual environment creation was completed.')
            return True
    except VenvCreateError:
        raise VenvCreateError

def install_requirements(path):
    venv_pip_dir = os.path.join(path,'venv','Scripts','pip.exe')
    print('Installing requirements...')
    try:
        if subprocess.run([venv_pip_dir,'install','-r','requirements.txt']):
            print('Requirements installed successfully.')
    except RequirementsInstallationError:
        raise RequirementsInstallationError
    
def show_types():
    print("Project types supported:")
    for type in sorted(PROJECT_TYPES):
        print(type.capitalize(),end='\n')    

def create_pyproject_file(path):
    data = generate_pyproject()
    get_or_create_file(path,'pyproject.toml',data)

