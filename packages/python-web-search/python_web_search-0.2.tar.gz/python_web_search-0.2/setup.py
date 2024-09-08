from setuptools import setup, find_packages

VERSION = '0.2'
DESCRIPTION = 'Perform a google search through the command line'
DEPENDENCIES = []

# Setting up
setup(
    name="python_web_search",
    version=VERSION,
    author="JanoKasu",
    author_email="ianandesmccracken@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=DEPENDENCIES,
    keywords=['python', 'search'],
	entry_points={
		"console_scripts": [
			"search = python_web_search:search",
        ]
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)