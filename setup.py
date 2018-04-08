import os
from setuptools import setup, find_packages


tests_require = [
    'tox',
    'pytest',
    'pytest-asyncio',
    'openapi-spec-validator',
]

extras_require = {
    'test': tests_require,
}

setup(
    name='oad',
    version='0.1',
    author='Vitaliy Nefyodov',
    author_email='vitent@gmail.com',
    license='Apache License 2.0',
    url='https://github.com/lordent/oad',
    description='Python library for generate valid OpenAPI v3 specification',
    long_description=open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'README.md'
        )
    ).read(),
    long_description_content_type='text/markdown',
    keywords='openapi openapi3 openapiv3 swagger python marshmallow',
    packages=find_packages(),
    data_files=[
        'LICENSE',
        'README.md',
    ],
    install_requires=['marshmallow'],
    tests_require=tests_require,
    extras_require=extras_require,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
    ]
)
