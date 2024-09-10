from setuptools import setup, find_packages

setup(
    name='oauthAzureFastApi',
    version='0.4.4',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'authlib',
        'httpx',
        'python-dotenv',
        'jose',
        'uvicorn',
        'starlette',
        'itsdangerous'
    ],
    description='A FastAPI module for Azure OAuth integration',
    long_description=open("README.md").read(),  # or README.rst
    long_description_content_type="text/markdown",  # or "text/x-rst"
    author='Saubhik Bhadra',
    author_email='saubhik.bhadra@gmail.com',
    url='https://github.com/saubhik1/oauthAzureFastApi',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)