import os

from setuptools import find_packages, setup


def read_version():
    with open("src/pyscript_dot_com/version") as f:
        return f.read().strip("\n")


def check_tag_version():
    if os.getenv("CHECK_VERSION", "false").lower() == "true":
        tag = os.getenv("GITHUB_REF")
        expected_version = read_version()
        if tag != f"refs/tags/{expected_version}":
            raise Exception(
                f"Tag '{tag}' does not match the expected "
                f"version '{expected_version}'"
            )


with open("README.md") as fh:
    long_description = fh.read()

check_tag_version()

setup(
    name="pyscript-dot-com-cli",
    version=read_version(),
    description="Command Line Interface for PyScript.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pyscript.com",
    author="Fabio Pliger, Nicholas Tollervey, Fabio Rosado, Madhur Tandon",
    author_email=(
        "fpliger@anaconda.com, "
        "ntollervey@anaconda.com, "
        "frosado@anaconda.com, "
        "mtandon@anaconda.com"
    ),
    license="Apache-2.0",
    install_requires=[
        "pyscript-cli==0.3.4",
        "pydantic==1.10.14",
        "requests==2.31.0",
        "keyring==24.3.1",
        "cryptography==42.0.5",
        "cffi==1.16.0",
        "python-dotenv==1.0.1",
        "pyjwt==2.8.0",
        "rich==13.4.1",
        "typer==0.9.0",
        "argon2-cffi==23.1.0; platform_system == 'Linux'",
        "pycryptodome==3.20.0; platform_system == 'Linux'",
        "keyrings.cryptfile==1.3.9; platform_system == 'Linux'",
        "SecretStorage>=3.3.3; platform_system == 'Linux'",
    ],
    extras_require={
        "tests": [
            "pytest==7.4.4",
            "pytest-recording==0.13.1",
            "vcrpy==6.0.1",
        ],
    },
    python_requires=">=3.9",
    keywords=["pyscript", "cli", "pyscript.com", "pyscript-cli", "pyscript-dot-com"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Pre-processors",
    ],
    entry_points={
        "pyscript": [
            "api = pyscript_dot_com",
        ],
    },
    project_urls={
        "Documentation": "https://docs.pyscript.net",
        "Examples": "https://pyscript.com/@examples",
        "Homepage": "https://pyscript.com",
        "Repository": "https://github.com/anaconda/pyscript-dot-com-issues",
    },
    zip_safe=False,
)
