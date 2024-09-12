from setuptools import setup, find_packages

setup(
    name='yooncloud-core',
    version='0.0.18',
    install_requires=['boto3', 'pydantic', 'urllib3<2,>=1.26.2', "pydash", "numpy", "pandas", "datetimerange"],
    packages=find_packages(),
    python_requires='>=3.8',
)