from setuptools import setup, find_packages # type: ignore

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
        name="libfunbox",
        version="1.09",
        author="kuba201",
        description='Orange Funbox 2.0 Wrapper',
        long_description=readme,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        url="https://flerken.zapto.org:1115/kuba/libfunbox",
        install_requires=["requests"],
        project_urls={
            'Source': 'https://flerken.zapto.org:1115/kuba/libfunbox',
        },
        keywords=['orange','router','funbox'],
        classifiers= [
            "Programming Language :: Python :: 3 :: Only",
            "License :: OSI Approved :: GNU General Public License (GPL)",
        ]
)