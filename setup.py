from setuptools import setup

def readme():
    with open('README.md') as file:
        README = file.read()
    return README


setup(
    name = 'aiotube',
    version = '1.2.0',
    description = 'Get YouTube Public Data without YouTubeAPI',
    long_description = readme(),
    long_description_content_type="text/markdown",
    package_dir={'aiotube': 'src'},
    packages=['aiotube'],
    install_requires = [
        'urllib3','youtube_dl'
    ],
    url = 'https://github.com/jnsougata/AioTube/blob/main/README.md',
    project_urls={
        "Bug Tracker": "https://github.com/jnsougata/AioTube/issues"
    },
    author = 'Sougata Jana',
    author_email = 'jnsougata@gmail.com',
    license = 'MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)
