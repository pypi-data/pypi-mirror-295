import argparse
from spider_cligen.commands import create_project_structure,show_types
from spider_cligen.utils import DEFAULT_CI_SERVICE,DEFAULT_LICENSE

def main():
    parser = argparse.ArgumentParser(description='Spider CLI')
    subparser =parser.add_subparsers(dest='command')

    create_project_structure_cmd = subparser.add_parser('startproject',help='Create a project structure')
    type_arg = subparser.add_parser('project-types',help='Show Supported project types.')

    args =  parser.parse_args()

    if args.command == 'startproject':
        project_type = input('Project Type:')
        project_name =  input('Project Name:')
        project_owner = input('Project Author:')
        owner_email = input('Author Email:')
        project_licence = input('Licence type[By default is used MIT]:') or DEFAULT_LICENSE
        ci_service = input('CI Service[By default is used Github Action]:') or DEFAULT_CI_SERVICE
        create_project_structure(project_type,project_name,project_licence,project_owner,owner_email,ci_service)    
    elif args.command == 'project-types':
        show_types()
if __name__ == '__main__':
    main()