from setuptools import setup, find_packages


# Leitura do conteúdo do README para a descrição longa
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="spider-cligen",
    version="0.1.0",
    author="Simão Domingos De Oliveira António",
    author_email="simaodomingos413@gamil.com",  
    description="A CLI tool to initialize Python projects with a standard structure.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simondev413/SpiderCLI", 
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[

    ],
    entry_points={
        'console_scripts': [
            'spider-cligen=spider_cligen.cli:main',  
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    tests_require=[
        "pytest",
    ],
    extras_require={
        "docs": [
            "sphinx",
        ],
        "test": [
            "pytest",
        ],
    },
    include_package_data=True, 
    project_urls={  
        "Source": "https://github.com/simondev413/SpiderCLI/",
    },
)
