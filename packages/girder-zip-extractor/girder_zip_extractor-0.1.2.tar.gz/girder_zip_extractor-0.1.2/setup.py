from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'girder>=3.0.0a1'
]

setup(
    author='Parth Sanghani',
    author_email='pas353@pitt.edu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    description='A Girder plugin to automatically extract uploaded zip files',
    install_requires=requirements,
    license='Apache Software License 2.0',
    long_description=readme,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='girder_plugin, zip_extractor',
    name='girder_zip_extractor',
    packages=find_packages(exclude=['test', 'test.*']),
    url='https://github.com/girder/zip_extractor',
    version='0.1.2',
    zip_safe=False,
    entry_points={
        'girder.plugin': [
            'zip_extractor = zip_extractor:GirderPlugin'
        ]
    }
)
