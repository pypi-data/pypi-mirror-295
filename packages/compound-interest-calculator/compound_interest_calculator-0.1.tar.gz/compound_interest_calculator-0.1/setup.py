from setuptools import setup, find_packages

setup(
    name='compound_interest_calculator',  # Nome do pacote
    version='0.1',
    description='Um pacote para calcular juros compostos em Python.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Gilberto Aparecido Bernardo Junior',
    author_email='gbernardoti@gmail.com',
    url='https://github.com/gbernardojr/compound_interest_calculator',  # Repositório
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
