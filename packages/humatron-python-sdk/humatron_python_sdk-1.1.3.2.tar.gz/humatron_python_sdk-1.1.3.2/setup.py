"""
" ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ████████╗██████╗  ██████╗ ███╗   ██╗
" ██║  ██║██║   ██║████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║
" ███████║██║   ██║██╔████╔██║███████║   ██║   ██████╔╝██║   ██║██╔██╗ ██║
" ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║   ██║██║╚██╗██║
" ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║╚██████╔╝██║ ╚████║
" ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"
"                   Copyright (C) 2023 Humatron, Inc.
"                          All rights reserved.
"""

from setuptools import setup


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='humatron-python-sdk',
    version='1.1.3.2',
    author='Humatron',
    author_email='worker_support@humatron.ai',
    description='SDK library for Humatron developers',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='http://humatron.ai/build/python_worker_sdk',
    packages=[
        'humatron',
        'humatron/worker',
        'humatron/worker/tools',
        'humatron/worker/tools/flask',
        'humatron/restclient'
    ],
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='Humatron python',
    python_requires='>=3.10'
)
