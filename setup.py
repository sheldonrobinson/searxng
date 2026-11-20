# SPDX-License-Identifier: AGPL-3.0-or-later
"""Installer for SearXNG package."""

from setuptools import setup, find_packages


def _read_brand_setting(key: str) -> str:
    """Read a single key from the brand section of searx/settings.yml.

    Parses the file directly instead of using PyYAML so that setup.py does
    not depend on PyYAML during an isolated wheel build.
    """
    with open('searx/settings.yml', encoding='utf-8') as f:
        in_brand = False
        for line in f:
            stripped = line.strip()
            if stripped == 'brand:':
                in_brand = True
                continue
            if in_brand:
                # stop when we leave the brand section (dedented line)
                if stripped and not line.startswith(' '):
                    break
                if ':' in stripped:
                    k, _, v = stripped.partition(':')
                    if k.strip() == key:
                        return v.strip().strip('"').strip("'")
    raise KeyError(f"brand.{key} not found in searx/settings.yml")


# Read version from searx/version.py directly (without importing the searx
# package, which would require runtime dependencies such as msgspec during
# an isolated wheel build).
version_ns: dict = {}
with open('searx/version.py', encoding='utf-8') as f:
    exec(f.read(), version_ns)
# Strip local version segment (e.g. '+b4a4b48') for PyPI compatibility.
# PyPI does not allow local version identifiers (PEP 440).
VERSION_TAG: str = version_ns['VERSION_TAG'].split('+')[0]
GIT_URL: str = version_ns['GIT_URL']

DOCS_URL: str = _read_brand_setting('docs_url')
ISSUE_URL: str = _read_brand_setting('issue_url')

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = [l.strip() for l in f.readlines()]

with open('requirements-dev.txt') as f:
    dev_requirements = [l.strip() for l in f.readlines()]

setup(
    name='searxng',
    description="SearXNG is a metasearch engine. Users are neither tracked nor profiled.",
    long_description=long_description,
    license="AGPL-3.0-or-later",
    author='SearXNG',
    author_email='contact@searxng.org',
    python_requires=">=3.10",
    version=VERSION_TAG,
    keywords='metasearch searchengine search web http',
    url=DOCS_URL,
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
    project_urls={"Code": GIT_URL, "Issue tracker": ISSUE_URL},
    entry_points={
        'console_scripts': ['searxng-run = searx.webapp:run']
    },
    packages=find_packages(
        include=[
            'searx',
            'searx.*',
            'searx.*.*',
            'searx.*.*.*',
        ]
    ),
    package_data={
        'searx': [
            'settings.yml',
            '*.toml',
            '*.msg',
            'data/*.json',
            'data/*.txt',
            'data/*.ftz',
            'favicons/*.toml',
            'infopage/**',
            'static/**',
            'templates/**',
            'translations/**',
        ],
    },
    install_requires=requirements,
    extras_require={'test': dev_requirements},
)
