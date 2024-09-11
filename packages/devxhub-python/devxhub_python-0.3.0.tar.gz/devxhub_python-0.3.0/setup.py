"""devxhub_python distutils configuration."""

from pathlib import Path

from setuptools import setup


def _get_version() -> str:
    """Read devxhub_python/VERSION.txt and return its contents."""
    path = Path("devxhub_python").resolve()
    version_file = path / "VERSION.txt"
    return version_file.read_text().strip()


version = _get_version()


with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()


requirements = [
    'binaryornot>=0.4.4',
    'Jinja2>=2.7,<4.0.0',
    'click>=7.0,<9.0.0',
    'pyyaml>=5.3.1',
    'python-slugify>=4.0.0',
    'requests>=2.23.0',
    'arrow',
    'rich',
]

setup(
    name='devxhub_python',
    version=version,
    description='A custom CLI for generating Django projects with devxhub_python templates',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Jamil Rayhan',
    author_email='jamil.rayhan.bsmrstu@gmail.com',
    url='https://github.com/git-jamil/devxhub_python',
    packages=['devxhub_python'],
    package_dir={'devxhub_python': 'devxhub_python'},
    entry_points={
        'console_scripts': [
            'devxhub_python = devxhub_python.__main__:main'
            ]
        },
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
    keywords=[
        "devxhub_python",
        "Python",
        "projects",
        "project templates",
        "Jinja2",
        "skeleton",
        "scaffolding",
        "project directory",
        "package",
        "packaging",
    ],
)
