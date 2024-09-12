from setuptools import setup, find_packages

setup(
    name='frstool',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
    ],
    include_package_data=True,
    description='Multi-package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='5sigma',
    author_email='support@5sigma.co',
    url='https://financialresiliencescore.com',
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)