from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="project-name",
    version="0.1.0",
    author="project_owner",
    author_email="owner_email",  
    description="exmple description.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/project-repository", 
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[

    ],
    entry_points={
        'console_scripts': [
            'project-name=project_name.main:main',  
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
        "Source": "https://github.com/project-repository",
    },
)