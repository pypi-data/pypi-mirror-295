from setuptools import setup, find_packages

setup(
    name='aamraz',
    version='0.0.1',
    author='Mohammad Mahmoodi Varnamkhasti',
    author_email='research@amzmohammad.com',
    description='This project is a collection of Natural Language Processing tools for Kurdish Language.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Change to 'text/x-rst' if using reStructuredText
    url='https://github.com/MohammadDevelop/Aamraz',  # URL to your project
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy>=2.1.0',
        'fasttext>=0.9.3',
    ],
)