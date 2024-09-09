from distutils.core import setup

from setuptools import find_packages


def parse_requirements(filename):
    """ 从requirements.txt中读取依赖项并排除带有选项的行 """
    with open(filename, 'r') as f:
        lines = f.readlines()
    reqs = []
    for line in lines:
        line = line.strip()
        # 忽略带有'--'的行
        if not line.startswith('--') and line:
            reqs.append(line)
    return reqs


setup(
    name='octopus-common-python',
    version='1.0.5c1',
    author='xzhao32',
    author_email='xzhao32@trip.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=parse_requirements("requirements.txt"),
)
