from setuptools import setup, find_packages

setup(
    name='eclipsetools',
    version='0.0.1',
    author='Matthew Sanchez',
    author_email='xxspicymelonxx@gmail.com',
    description='A set of useful custom tools that I use a lot',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[
	'opencv-python',
	'pillow',
	'numpy'
    ],
)
