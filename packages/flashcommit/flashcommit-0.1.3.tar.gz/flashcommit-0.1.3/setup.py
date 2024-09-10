from setuptools import setup, find_packages

setup(
    name='flashcommit',
    version='0.1.3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fcommit=flashcommit.main:main',
        ],
    },
    python_requires=">=3.8.0",
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
