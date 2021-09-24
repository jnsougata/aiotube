from setuptools import setup

def readme():
    with open('README.md') as file:
        README = file.read()
    return README


setup(
    name = 'dya',
    version = '3.6.5',
    description = 'Get Unlimited YouTube Public Data without YouTubeAPI',
    long_description = readme(),
    long_description_content_type="text/markdown",
    package_dir={'dya': 'source'},
    packages=['dya'],
    install_requires = [
        'urllib3'
    ],
    url = 'https://github.com/jnsougata/Ditch-YouTubeAPI/blob/main/README.md',
    project_urls={
        "Bug Tracker": "https://github.com/jnsougata/Ditch-YouTubeAPI/issues"
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
