#!/usr/bin/env python3
"""
A converter from PlantUML class diagrams to python3 skeleton classes.
"""

import setuptools

with open("README.md", "r") as fh:
	readme = fh.read()

setuptools.setup(name='uml2py', # 'uml2py-pkg-peresan',
	version='1.0.1',
	author='Pedro Reis dos Santos',
	author_email="reis.santos@tecnico.ulisboa.pt",
	description="A converter from PlantUML class diagrams to python3 skeleton classes.",
	long_description=readme,
	long_description_content_type="text/x-rst",
	license = 'MIT',
	url="https://github.com/pedroreissantos/uml2py",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Compilers',
		'Development Status :: 4 - Beta',
		'Environment :: Console',
	],
	python_requires='>=3.8',
	install_requires=[ 'ply', 'plantuml' ],
	py_modules = [ 'uml2py' ],
	packages=setuptools.find_packages(),
)
