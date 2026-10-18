# SPDX-License-Identifier: AGPL-3.0-or-later
"""Installer for SearXNG package."""

import os
from setuptools import setup, find_packages

# Resolve paths relative to this setup.py file so builds work in isolated
# environments (CI, pip install from sdist, etc.)
_here = os.path.dirname(os.path.abspath(__file__))


def _read_file(filename, default=""):
    """Read a file relative to setup.py, returning default if missing."""
    try:
        with open(os.path.join(_here, filename), encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return default


def _read_lines(filename):
    """Read non-empty lines from a file relative to setup.py."""
    text = _read_file(filename)
    return [l.strip() for l in text.splitlines() if l.strip()]


# Version info - fall back gracefully when git is not available (CI builds)
try:
    from searx.version import VERSION_TAG, GIT_URL
except Exception:  # pylint: disable=broad-except
    VERSION_TAG = "0.0.0"
    GIT_URL = "unknown"


# Settings - fall back gracefully when searx package is not importable
try:
    from searx import get_setting

    _docs_url = get_setting("brand.docs_url")
    _issue_url = get_setting("brand.issue_url")
except Exception:  # pylint: disable=broad-except
    _docs_url = ""
    _issue_url = ""

long_description = _read_file("README.rst")
requirements = _read_lines("requirements.txt")
dev_requirements = _read_lines("requirements-dev.txt")

setup(
    name="searxng",
    description="SearXNG is a metasearch engine. Users are neither tracked nor profiled.",
    long_description=long_description,
    license="AGPL-3.0-or-later",
    author="SearXNG",
    author_email="contact@searxng.org",
    python_requires=">=3.10",
    version=VERSION_TAG,
    keywords="metasearch searchengine search web http",
    url=_docs_url,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    project_urls={"Code": GIT_URL, "Issue tracker": _issue_url},
    entry_points={"console_scripts": ["searxng-run = searx.webapp:run"]},
    packages=find_packages(
        include=[
            "searx",
            "searx.*",
            "searx.*.*",
            "searx.*.*.*",
        ]
    ),
    package_data={
        "searx": [
            "settings.yml",
            "*.toml",
            "*.msg",
            "data/*.json",
            "data/*.txt",
            "data/*.ftz",
            "favicons/*.toml",
            "infopage/**",
            "static/**",
            "templates/**",
            "translations/**",
        ],
    },
    install_requires=requirements,
    extras_require={"test": dev_requirements},
)
