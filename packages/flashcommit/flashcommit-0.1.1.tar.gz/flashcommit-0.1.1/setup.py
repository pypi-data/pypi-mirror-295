from setuptools import setup, find_packages

setup(
    name='flashcommit',
    version='0.1.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fcommit=flashcommit.main:main',
        ],
    },
    install_requires=[
        'setuptools',
        'requests',
        'argparse',
        'pydantic',
        'gitpython',
        'pydriller',
        'python-dotenv~=1.0.1',
        'websocket-client',
        'rich',
        'prompt_toolkit',
    ],
)
