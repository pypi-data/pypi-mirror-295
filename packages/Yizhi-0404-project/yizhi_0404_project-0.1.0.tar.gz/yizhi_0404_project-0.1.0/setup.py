from setuptools import setup, find_packages
from typing import List

Hyphen_e = '-e .'

# def get_requirements(filename: str) -> List[str]:
#     requirements = []
#     with open(filename) as obj:
#         requirements = obj.readline()
#         requirements = [req.replace("\n", "") for req in requirements]
        
#         if Hyphen_e in requirements:
#             requirements.remove(Hyphen_e)
            
#     return requirements

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name = "Yizhi_0404_project",
    version="0.1.0",
    author="Cloud",
    author_email="2001maki0419@gmail.com",
    long_description=long_description,
    url=f'https://github.com/maki2131/ML_OPS.git',
    #install_requires=get_requirements("requirements.txt"),
    package_dir={"": "src"},
    packages=find_packages(where="src")
)