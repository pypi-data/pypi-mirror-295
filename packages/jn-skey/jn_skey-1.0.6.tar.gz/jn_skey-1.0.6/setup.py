from setuptools import setup, find_packages

setup(
    name='jn-skey',  # The name of your package
    version='1.0.6',  # Added slight delay
    packages=find_packages(),  # Automatically find packages in your directory
    entry_points={
        'console_scripts': [
            'jn-skey = jn_skey.jn_skey:main',
        ],
    },
    install_requires=[
        'pynput',  # Add any dependencies your package needs
    ],
    author='Costa Rica Makers',
    author_email='webmaster@costaricamakers.com',
    description='A tool to insert the current datetime using a keyboard shortcut.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/jn-skey',  # Replace with your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the Python versions supported
)
