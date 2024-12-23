from typing import List
from setuptools import find_packages, setup

HYPHEN_E_DOT = "-e ."


def get_requirements(file_path: str) -> List[str]:
    """
    This function will return the list of requirements
    """
    requirements = []
    with open(file_path, encoding="utf-8") as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


setup(
    name="fifthwall_cyber_loss_estimation",
    version="0.0.1",
    author="David P.",
    author_email="cognition.pasted392@aleeas.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)
