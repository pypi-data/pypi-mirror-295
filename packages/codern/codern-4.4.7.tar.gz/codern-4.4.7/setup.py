from setuptools import setup, find_packages

def read_file(filename):
    with open(filename, encoding='utf-8') as f:return f.read()

setup(
    name='codern',
    version='4.4.7',
    packages=find_packages(),
    install_requires=[
        'requests',
        'httpx',
        'bs4',
        'urllib3',
        'pycryptodome',
        'pillow',
    ],
    include_package_data=True,
    description='Codern Team Library from api free O - > api-free.ir',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://api-free.ir',
    author='Mahdi Ahmadi',
    author_email='mahdiahmadi.1208@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
