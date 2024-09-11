from setuptools import setup, find_packages

setup(
    name="blikon_sdk",
    version="1.0.3",
    packages=find_packages(include=['blikon_sdk', 'blikon_sdk.*']),
    install_requires=[
        "fastapi",
        "pydantic-settings",
        "uvicorn",
        "google-auth",
        "google-cloud-firestore",
        "httpx",
        "python-dotenv",
        "pydantic[email]",
        "jose",
        "firebase-admin",
        "pyjwt",
        "cryptography"
    ],
    description="Blikon SDK for cryptography, security, and middleware services",
    author="Raúl Díaz Peña",
    author_email="rdiaz@yosoyblueicon.com",
    license="Blikon Ⓡ",
    url="https://github.com/blikon/blikon_sdk",
)