from setuptools import setup, find_packages

setup(
    name="ToyLang",
    version="1.0.0",
    description="A simple scripting language interpreter",
    author="ToyLang Raja",
    author_email="toylang001@gmail.com",
    url="https://github.com/toylang001/toylang",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'toylang=toylang.interpreter:main',  # This allows you to run the interpreter from the command line
        ],
    },
    install_requires=[
        # List of dependencies (if any)
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
