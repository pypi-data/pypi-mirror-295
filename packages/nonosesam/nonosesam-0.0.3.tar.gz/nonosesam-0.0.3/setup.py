from setuptools import setup, find_packages

setup(
    name="nonosesam",
    version="0.0.3",
    packages=find_packages(),
    install_requires=[
        'python-dotenv',  # Environment variable management
        'cryptography',   # Encryption library
        'pytest',         # Testing framework
    ],
    author='Miguel Lopez',
    author_email='miguel@lopezmartin.me',
    description='A flexible secret management system',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lopezmartin/sesam',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9'
)

