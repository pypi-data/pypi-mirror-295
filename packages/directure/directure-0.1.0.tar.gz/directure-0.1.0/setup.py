from setuptools import setup, find_packages

setup(
    name='directure',  # Package name
    version='0.1.0',  # Initial version
    description='A tool to explore and visualize directory structures',  # Short description
    long_description=open('README.md').read(),  # Detailed description (shown on PyPI)
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/directure',  # URL of your project (GitHub link)
    author='Your Name',
    author_email='your.email@example.com',
    license='MIT',  # Choose a license
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version
    entry_points={
        'console_scripts': [
            'directure=directure.directure:main',  # This makes 'directure' executable from the command line
        ],
    },
)
