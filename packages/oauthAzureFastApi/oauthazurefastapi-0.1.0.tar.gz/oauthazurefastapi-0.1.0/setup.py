from setuptools import setup, find_packages

setup(
    name="oauthAzureFastApi",
    version="0.1.0",
    description="A FastAPI OAuth2 module with Azure AD",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "httpx",
        "authlib",
        "python-dotenv",
        "python-jose",
        "starlette",
    ],
    author="Saubhik Bhadra",
    author_email="saubhik.bhadra@gmail.com",
    url="https://github.com/saubhik1/azure-oauth-fastapi",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)