from setuptools import find_packages,setup #This imports tools to help you package your Python project 
#so others (or you) can install it like any library (numpy, pandas, etc.)




# setup(
# name='mlproject',
# version='0.0.1',
# author='dibimaiga',
# author_email='dibimaigapro@gmail.com',
# packages=find_packages(),
# install_requires=['pandas','numpy','seaborn'] # for all the libraries I want, it will be installed automatically

# )

# With this setup how it will be able to find out how many packages are in the projects ?
# We will create a new folder "src" and in it we're going to create a new_file init.py because we want to 
# find the "src" as package 

# And so if we run "find_packages()", it will go and see how many folder we have in this underscore init.
# So itwill directly consider "src" as a package and we'll try to build  it and once built,you can probably
# import it anywhere like with pandas or numpy. 

# But for really that we need to put it in the py py package itself
# However in order to make sure that this gets build out of the package itself, we'll be using "__init__"
# and try will to create this particular file "__init__.py"

from typing import List

HYPHEN_E_DOT = "-e ."

def get_requirements(file_path:str)-> List[str]:
    """
    This function will return a list of requirements

    """
    requirements = []
#we are going to open the file containing the requirements
    with open(file_path) as file_obj: #(#as a temporary file object)
        requirements = file_obj.readlines()

        requirements = [req.replace("\n","") for req in requirements] 

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    return requirements


setup(
name='mlproject',
version='0.0.1',
author='dibimaiga',
author_email='dibimaigapro@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt') # for all the libraries I want, it will be installed automatically

)