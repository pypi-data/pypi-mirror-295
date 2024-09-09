Spider CLIGEN Documentation

## Overview
The **Spider CLIGEN** is a command-line tool that helps developers quickly set up different types of Python projects, including packages, web applications, mobile apps, and more. It automates the creation of project structures, virtual environments, and essential files such as `README.md`, `.gitignore`, `LICENSE`, and CI workflow files for services like GitHub Actions, GitLab CI, and CircleCI.

### Main Features:
- Create project structure based on different types of Python projects.
- Support for multiple license types (MIT, GPLv3, Apache, BSD 3-Clause, CC0).
- Automates the creation of a virtual environment and installation of dependencies.
- Generates configuration files for popular CI services.
- Automatically generates essential files like `README.md`, `.gitignore`, `LICENSE`, and more.

## Usage

The CLI provides the following commands:

- `startproject`: Initialize a new project structure.
- `project-types`: Display the supported project types.

### Example

```bash
# Start a new project
$ python spider_cligen startproject

# Show supported project types
$ python spider_cligen project-types
```

### Licenses Supported

- MIT
- Apache 2.0
- BSD 3 Clause
- CCO
- GPLv3
