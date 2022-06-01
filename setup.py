from setuptools import setup

setup(
    name='aiobotstat',
    version='0.1',
    url='https://github.com/viuipan/aiobotstat',
    author_email='viuipan@gmail.com',
    license='MIT',
    description='Library for api.botstat.io',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=['aiobotstat', 'aiobotstat.models'],
    setup_requires=['aiohttp', 'pydantic', 'certifi', 'ujson']
)
