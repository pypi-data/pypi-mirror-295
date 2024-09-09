from setuptools import setup, find_packages

setup(
    name='d-link',
    version='0.1',
    author='Pg Network',
    author_email='gamerzp780@gmail.com',
    description='A Python library to extract data from a Python script and push it to a GitHub Pages repository.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PgNetwork01/d-link',  # Update with your repository URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # List any dependencies here
        # Example: 'requests>=2.25.1'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
