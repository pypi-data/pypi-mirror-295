from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='sophi-app-internal',
    version='0.1.13',
    packages=find_packages(where='.', include=['sophi_app_internal', 'sophi_app_internal.*']),
    install_requires=[
        'requests',
        'pyjwt',
        'cryptography',
        'python-jose',
        'pydantic',
        'azure-cosmos',
        'python-dotenv',
        'auth0-python',
        'google-api-python-client',
        'google-auth-oauthlib',
        'azure-storage-blob',
        'slack_sdk'
    ],
    long_description=description,
    long_description_content_type="text/markdown"
)