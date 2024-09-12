from setuptools import setup, find_packages

setup(
    name = 'python-window-recorder',
    packages=find_packages(),
    install_requires=['opencv-python', 'pywin32'],
    version = '0.8',
    description = 'Background window recorder',
    url = 'https://github.com/xjxckk/window-recorder/',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
    )