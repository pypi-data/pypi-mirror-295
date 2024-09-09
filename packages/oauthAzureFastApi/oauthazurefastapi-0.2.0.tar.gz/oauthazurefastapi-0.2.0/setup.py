from setuptools import setup, find_packages

setup(
    name='oauthAzureFastApi',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'authlib',
        'httpx',
        'python-dotenv',
        'jose',
        'uvicorn'
    ],
    description='A FastAPI module for Azure OAuth integration',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/azure_oauth_fastapi',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)