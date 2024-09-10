from setuptools import setup, find_packages

setup(
    name='animegirlapi',
    version='1.6.0',
    packages=find_packages(),  # This should find the 'animegirlapi' directory
    install_requires=[
        'requests>=2.25.1',
    ],
    description='An API that can output anime girls, and is 100% manually verified',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Alleexx',
    author_email='Alleexx129@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
