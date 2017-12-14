from setuptools import setup
'''
Tool to automatically tag Chain References and Cross References
'''

setup(
    name="CrossRefTag",
    description="To automatically tag Chain Bible References\
    and Cross Refernces with info from Biblical Terms",
    long_description=open("README.md").read(),
    version="0.1dev",
    license="MIT",
    packages=["CrossRefTag",],
    install_requires=[
        "joblib",
        "nltk"
        ],
)
