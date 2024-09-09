from setuptools import setup, find_packages

VERSION = '1.4.0'


# Setting up
setup(
    name="pryvx_ml",
    version=VERSION,
    author="PryvX (Jayesh Kenaudekar)",
    author_email="<jayesh@pryvx.com>",
    description="Federated Learning python library",
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
        'requests',
    ],
    keywords=['python', 
              'privacy-preserving', 
              'federated-learning', 
              'machine-learning'],

    classifiers=[
        'Programming Language :: Python :: 3.9',
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    include_package_data=True,
)