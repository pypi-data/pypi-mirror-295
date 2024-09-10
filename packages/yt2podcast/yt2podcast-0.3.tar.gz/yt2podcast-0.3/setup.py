from setuptools import setup, find_packages

setup(
    name = 'yt2podcast',
    version = '0.3',
    packages = find_packages(include = ['yt2podcast', 'yt2podcast.*']),
    include_package_data=True,
    install_requires = [
        "requests",
        "pyperclip",
        "dropbox",
    ],
)