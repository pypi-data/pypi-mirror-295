from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='aniwatch-tr',
    version='0.3.4',
    install_requires=[
        'requests',
        'inquirer',
    ],
    author='deodorqnt',
    author_email='noronneural@gmail.com',
    description='Terminalden türkçe anime izleme, indirme',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/username/aniwatch-tr',
    license="GPLv3",
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    entry_points={
        'console_scripts': [
            'aniwatch-tr=aniwatch_tr.main:main',
        ],
    },
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.10',
)