from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
    name='FrameBuilder',
    version='0.1.1',
    description='Library for creating projects with a ready-made structure on popular Python frameworks',
    author='Ibragimov Zabit',
    author_email='xaclafun1991@gmail.com',
    url='https://github.com/zabit923/FrameBuilder',
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'rich',
        'inquirerpy'
    ],
    entry_points={
        'console_scripts': [
            'builder-run=builder.core:command_run',
            'builder-rebuild=builder.core:command_rebuild',
            'builder-help=builder.core:command_help',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
)
