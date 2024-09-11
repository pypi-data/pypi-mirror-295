from setuptools import setup, find_packages

setup(
    name="positron_networks",
    version="0.1.14",
    description="Run experiments on the Positron Cloud",
    author="Balint Kerdi",
    author_email="bkerdi@positronnetworks.com",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(where="app"),
    package_dir={"": "app"},
    package_data={
        'positron_common': ['build_env'],
    },
    install_requires=[
        'requests>=2.20.0,<3.0.0',
        'python-socketio>=5.0.0,<6.0.0',
        'colorama>=0.4.0,<1.0.0',
        'configparser>=5.0.0,<7.0.0',
        'argparse>=1.4.0',
        'aiohttp>=3.7.4.post0',
        'typer>=0.12.3',
        'pyyaml>=6.0.1',
        'pydantic>=2.8.0',
        'pydantic_core>=2.20.0',
        's3transfer>=0.10.0',
        'boto3>=1.34.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'positron=positron_cli.cli:app',
            'positron-job-runner=positron_job_runner.cli:app',
        ],
    },
    python_requires='>=3.6',
    license='Apache License 2.0',
)
