from setuptools import setup, find_packages


setup(
    name="fast-knifes",
    version="0.0.41",
    author="knifes",
    author_email="author@example.com",
    description="Fast Swiss Army Knife",
    long_description="`pip install fast-knifes --index-url https://pypi.python.org/simple -U`",
    long_description_content_type="text/markdown",
    url="https://github.com/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "attrs",  #  required by knifes/jsons.py
        "cattrs",  #  required by knifes/jsons.py
        "anyio",  # required by knifes/shell.py
        "typer",  # required by deploy module
        "python-dotenv",  # required by deploy module
        # "gevent",  # required by deploy/celery module
        # "httpx[http2]",
        # 'cryptography',  #  required by aes
    ],
    entry_points={
        "console_scripts": [
            "deploy = knifes.deploy.main:app",
        ],
    },
)
