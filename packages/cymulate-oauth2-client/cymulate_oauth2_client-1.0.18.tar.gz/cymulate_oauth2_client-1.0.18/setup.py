from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cymulate_oauth2_client',
    version='1.0.18',
    description='A Python client for OAuth2 authentication with the Cymulate API. This library simplifies the process of authenticating with the Cymulate API using OAuth2, managing tokens, and making secure requests effortlessly.',
    author='Cymulate',
    author_email='roys@cymulate.com',
    url='https://github.com/cymulate-ltd/oauth2-client',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    install_requires=[
        'requests>=2.31.0, <3',
        'tenacity>=8.2.2, <9',
        'urllib3>=2.0.6, <3',
        'aiohttp>=3.8.6, <4',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Natural Language :: English',
    ],
    python_requires='>=3.12',
    extras_require={
        'dev': [
            'pytest>=7.4.0, <8',
            'pytest-asyncio>=0.21.0, <0.22',
            'flake8>=6.1.0, <7',
            'black>=23.7.0, <24',
        ],
    },
    entry_points={
        'console_scripts': [
            'cymulate-cli=cymulate_oauth2_client.cli:main',  # Example of a command-line tool
        ],
    },
    project_urls={
        'Documentation': 'https://github.com/cymulate-ltd/oauth2-client#readme',
        'Bug Tracker': 'https://github.com/cymulate-ltd/oauth2-client/issues',
        'Source Code': 'https://github.com/cymulate-ltd/oauth2-client',
    },
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',  # Assuming you have a tests/ directory with your test code
)