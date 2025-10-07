# This file will create a Meta Data as a project details package


from setuptools import find_packages, setup
from typing import List


HYPEN_E_DOT = "-e ."


# Define what this module does , reading the laibraries line by line from requirements.txt
def get_requirements(file_path: str) -> List[str]:
    """
    This function will return the list of requirements from requirements.txt file
    """
    requirements = []  # Create an empty list
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements  # return always will be at last


# Project details / Meta data
setup(
    name="mlproject",
    version="0.0.1",
    author="pratap",
    author_email="pratap.jadhav0@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)
