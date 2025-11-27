from setuptools import find_packages, setup
from typing import List 

def get_requirements()->List[str]:
    """
    This function will return the list of requirements
    """
    requirement_list:List[str] = []
    try :
        #opening the file and read the requirements
        with open('requirements.txt','r') as f:
            lines = f.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("file not found")
    
    return requirement_list

print(get_requirements())

setup(
    name="Trip_mate",
    version="0.0.1",
    author="amil",
    author_email="amilasnils008@gmail.com",
    packages= find_packages(),
    install_requires= get_requirements(),
)

            