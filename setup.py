from setuptools import setup, find_packages

setup(
    name='iudx',
    version='2.0.1',
    packages=find_packages(),
    install_requires=['requests', 'urllib3', 'pandas', 'click'],
    entry_points={
        "console_scripts": [
            "iudx=iudx.entity.Entity:Entity.cli",
        ],
    },
    url='https://github.com/datakaveri/iudx-python-sdk',
    license='GNU General Public License v3.0',
    author='Paras V, Sreekrishnan, Rakshit R',
    author_email='rakshit.rameshd@datakaveri.org',
    description='Python SDK for IUDX.'
    )

