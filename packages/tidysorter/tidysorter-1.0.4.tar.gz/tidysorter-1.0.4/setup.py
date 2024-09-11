from setuptools import setup, find_packages

setup(
    name='tidysorter',
    version='1.0.4',
    author='Arnaud Le Floch',
    author_email='a.lefloch2491@gmail.com',
    description='A tool to organize files in a directory',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ale-floc/tidysorter',
    packages=find_packages(),
    entry_points={'console_scripts': ['tidysorter=tidysorter.tidysorter:main']},
    install_requires=[]
)