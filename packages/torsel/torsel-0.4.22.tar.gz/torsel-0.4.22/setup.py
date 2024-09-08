from setuptools import setup, find_packages
setup(
    name='torsel',
    version='0.4.22',
    description='A Python module for managing Tor instances with Selenium',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='azuk4r',
    author_email='azuk4r@tuta.io',
    url='https://github.com/azuk4r/torsel',
    packages=find_packages(include=['torsel', 'torsel.*']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.8',
    install_requires=[
        'selenium',
        'stem',
    ],
    keywords='tor selenium web scraping automation',
    include_package_data=True,
    zip_safe=False,
)