from setuptools import setup, find_packages

print(find_packages(include=['restack_sdk_cloud', 'restack_sdk_cloud.*', 'assertions', 'assertions.*']))

setup(
    name='restack_sdk_cloud',
    version='1.0.3',
    description='Deploy to Restack with cloud SDK',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    author='Restack',
    author_email='',
    url='https://github.com/restackio/restack-sdk-cloud-py',
    packages=find_packages(),
    install_requires=[
        'colorama',
        'GitPython',
        'pydantic',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
