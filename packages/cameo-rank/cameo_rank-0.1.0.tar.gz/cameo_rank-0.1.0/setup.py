from setuptools import setup, find_packages

setup(
    name='cameo_rank',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'pydantic',
        'uvicorn',
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
    author='JcXGTcW',
    author_email='jcxgtcw@gmail.com',
    description='A Python package for managing game rankings using FastAPI.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/JcXGTcW/cameo_rank',
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)