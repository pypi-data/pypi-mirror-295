from setuptools import setup, find_packages

setup(
    name='oauthAzureFastApi',
    version='0.3.0',
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
    author='Saubhik Bhadra',
    author_email='saubhik.bhadra@gmail.com',
    url='https://github.com/yourusername/azure_oauth_fastapi',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)