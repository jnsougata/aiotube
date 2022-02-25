import pathlib
from setuptools import setup, find_packages


here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name='aiotube',
    version='1.4.8',
    description='Access YouTube Public Data without YouTubeAPI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jnsougata/aiotube',
    author='jnsougata',
    author_email='jnsougata@gmail.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='youtube, youtube-data, youtube-api, youtube-data-api-v3',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=['urllib3'],
    project_urls={
        'Bug Reports': 'https://github.com/jnsougata/aiotube/issues',
        'Source': 'https://github.com/jnsougata/aiotube',
    },
)
