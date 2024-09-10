from setuptools import setup, find_packages

setup(
    name='open-ortho-terminology',  # Package name, should be unique on PyPI
    version='0.3.3',  # Package version
    author='Toni Magni',  # Your name or your organization's name
    author_email='open-ortho@case.edu',  # Your contact email
    description='A package for managing orthodontic codes and namespaces.',  # Short description
    long_description=open('README.md').read(),  # Long description from README.md
    long_description_content_type='text/markdown',  # Specifies that the long description is in Markdown
    url='https://github.com/open-ortho/codes',  # Project home page or repository URL
    packages=find_packages(),  # Automatically find and include all packages in the project
    classifiers=[  # Classifiers help users find your project based on its characteristics
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Healthcare Industry',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',  # Assuming MIT, change as necessary
        'Programming Language :: Python :: 3',  # Specify the Python versions supported
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='orthodontics codes fhir healthcare snomed',  # Keywords to make your project more discoverable
    install_requires=[],
    python_requires='>=3.6',  # Minimum Python version required
    include_package_data=True,  # Include other files specified in MANIFEST.in
    # package_data={'yourpackage': ['data/*.dat']},  # Include specific package data
    entry_points={  # Allows you to create command-line scripts
        'console_scripts': [
            'oo-codes=open_ortho_terminology.main:main', 
        ],
    },
)
