from setuptools import find_packages, setup
from typing import List

# Define a constant for the hyphen-e-dot string 
HYPEN_E_DOT='-e .'
def get_requirements(file_path: str) -> List[str]:
    """
    This function takes a file path as input and returns a list of requirements
    from the requirements.txt file.
    """
    # Create an empty list to store the requirements
    requirements = []

    # Open the file using the 'with' statement located at 'file_path'
    with open(file_path) as file_obj:
        # Read the lines from the file and store them in the 'requirements' list
        requirements = file_obj.readlines()

    # Replace the newline character from each requirement 
    requirements = [req.replace("\n", "") for req in requirements]

    # If the '-e .' requirement is in the list, remove it
    if HYPEN_E_DOT in requirements:
        requirements.remove(HYPEN_E_DOT)

    # Return the list of requirements
    return requirements

setup(
name = 'mlproject',
version = '0.1',
author = 'Minich',
author_email = 'minichworks@gmail.com',
description = 'A machine learning project for predicting employee perfomance',
packages = find_packages(),
install_requires = get_requirements('requirements.txt')
)


