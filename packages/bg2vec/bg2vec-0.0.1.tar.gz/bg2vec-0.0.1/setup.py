from setuptools import setup, find_packages

setup(
    name='bg2vec',
    version='0.1.0',
    description='Bg2Vec is a sentence transformer for the bulgarian language',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/your_project_name',
    packages=find_packages(),
    install_requires=[
        'llm2vec'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)